from pathlib import Path
from ultralytics import YOLO


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "ppe_detector.pt"
)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Production model not found: {MODEL_PATH}"
        )

    return YOLO(str(MODEL_PATH))