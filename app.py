import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import tempfile
from pathlib import Path
import av

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


MODEL_PATH = r"D:\Yolo\runs\detect\runs\benchmark\yolov8n\weights\best.pt"
# Use YOLOv8n for webcam. Use heavier models for image/video only.


st.set_page_config(
    page_title="YOLOv8 PPE Detection",
    page_icon="🦺",
    layout="wide"
)


@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)


model = load_model()


st.sidebar.title("Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.10,
    0.90,
    0.35,
    0.05
)

iou = st.sidebar.slider(
    "IoU Threshold",
    0.10,
    0.90,
    0.60,
    0.05
)

mode = st.sidebar.radio(
    "Inference Mode",
    ["Image", "Video", "Webcam"]
)


st.title("YOLOv8 PPE Detection System")
st.write("Computer vision demo for PPE detection using YOLOv8.")
st.markdown("---")


if mode == "Image":
    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:
        image = Image.open(uploaded_image).convert("RGB")
        image_np = np.array(image)

        results = model.predict(
            source=image_np,
            conf=confidence,
            iou=iou,
            verbose=False
        )

        annotated = results[0].plot()
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Original Image", use_container_width=True)

        with col2:
            st.image(annotated, caption="YOLOv8 Detection", use_container_width=True)


elif mode == "Video":
    uploaded_video = st.file_uploader(
        "Upload a video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_video is not None:
        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_input.write(uploaded_video.read())
        input_video_path = temp_input.name

        cap = cv2.VideoCapture(input_video_path)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_video_path = temp_output.name

        writer = cv2.VideoWriter(
            output_video_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress = st.progress(0)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            results = model.predict(
                source=frame,
                conf=confidence,
                iou=iou,
                verbose=False
            )

            annotated_frame = results[0].plot()
            writer.write(annotated_frame)

            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            if total_frames > 0:
                progress.progress(min(current_frame / total_frames, 1.0))

        cap.release()
        writer.release()

        st.success("Video processing completed.")
        st.video(output_video_path)


elif mode == "Webcam":
    st.subheader("Live Webcam Detection")

    st.warning(
        "Use YOLOv8n for webcam mode. Heavier models may be too slow for live detection."
    )

    class YOLOVideoProcessor(VideoProcessorBase):
        def recv(self, frame):
            image = frame.to_ndarray(format="bgr24")

            results = model.predict(
                source=image,
                conf=confidence,
                iou=iou,
                imgsz=416,
                verbose=False
            )

            annotated = results[0].plot()

            return av.VideoFrame.from_ndarray(annotated, format="bgr24")

    webrtc_streamer(
        key="ppe-webcam",
        video_processor_factory=YOLOVideoProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        async_processing=True
    )