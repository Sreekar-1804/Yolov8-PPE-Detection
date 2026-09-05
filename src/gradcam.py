import torch
import torch.nn.functional as F


class YOLOGradCAM:

    def __init__(self, yolo_model, layer_id=21):

        self.model = yolo_model.model
        self.model.eval()

        # Keep backbone/neck in evaluation mode,
        # but make Detect return raw differentiable outputs.
        self.detect = self.model.model[-1]
        self.detect.train()

        self.activation = None
        self.gradient = None

        layer = self.model.model[layer_id]

        self.hook = layer.register_forward_hook(
            self._capture_activation
        )

    def _capture_activation(self, module, inputs, output):

        self.activation = output

        if output.requires_grad:
            output.register_hook(
                self._capture_gradient
            )

    def _capture_gradient(self, gradient):
        self.gradient = gradient

    def generate(self, image_tensor):

        self.activation = None
        self.gradient = None

        self.model.zero_grad()

        image_tensor = (image_tensor.detach().requires_grad_(True))

        with torch.enable_grad():

            outputs = self.model(image_tensor)

            if not isinstance(outputs, dict):
                raise TypeError(f"Expected dict output, got {type(outputs)}")

            target = outputs["scores"].sigmoid().max()

            target.backward()

        if self.activation is None:
            raise RuntimeError("Activation not captured.")

        if self.gradient is None:
            raise RuntimeError("Gradient not captured.")

        weights = self.gradient.mean(dim=(2, 3),keepdim=True)

        cam = (weights * self.activation).sum(dim=1,keepdim=True)

        cam = F.relu(cam)

        cam = F.interpolate(cam,size=image_tensor.shape[-2:],mode="bilinear",align_corners=False)

        cam = cam[0, 0]

        cam -= cam.min()
        cam /= cam.max() + 1e-8

        return cam.detach().cpu().numpy()

    def close(self):

        self.hook.remove()
        self.detect.eval()