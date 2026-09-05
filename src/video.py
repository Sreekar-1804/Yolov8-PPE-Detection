import cv2
import tempfile
from pathlib import Path

from src.inference import predict_frame


def process_video(model, uploaded_file, confidence=0.25):

    input_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    input_file.write(
        uploaded_file.read()
    )

    input_file.close()

    input_path = Path(input_file.name)

    output_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    output_file.close()

    output_path = Path(output_file.name)

    cap = cv2.VideoCapture(
        str(input_path)
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    while True:

        success, frame = cap.read()

        if not success:
            break

        annotated = predict_frame(
            model,
            frame,
            confidence
        )

        writer.write(
            annotated
        )

    cap.release()
    writer.release()

    return output_path