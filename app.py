import streamlit as st
from PIL import Image

from src.model import load_model
from src.inference import predict_image
from src.video import process_video


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Industrial PPE Detection",
    page_icon="🦺",
    layout="wide"
)


# --------------------------------------------------
# Model loading
# --------------------------------------------------

@st.cache_resource
def get_model():
    return load_model()


model = get_model()


# --------------------------------------------------
# Minimal styling
# --------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .app-subtitle {
            font-size: 1.05rem;
            opacity: 0.75;
            margin-bottom: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("Industrial PPE Detection")

st.markdown(
    """
    <div class="app-subtitle">
        YOLOv8-based workplace safety monitoring for PPE compliance
        and unsafe-condition detection.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Sidebar settings
# --------------------------------------------------

with st.sidebar:

    st.header("Detection Settings")

    confidence = st.slider(
        "Confidence Threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.25,
        step=0.05
    )

    st.caption(
        "Higher values reduce low-confidence detections."
    )

    st.divider()

    st.subheader("Supported Classes")

    st.markdown(
        """
        - Hardhat
        - Safety Vest
        - NO-Hardhat
        - NO-Safety Vest
        - Person
        """
    )


# --------------------------------------------------
# Project summary
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Model", "YOLOv8")
col2.metric("PPE Classes", "5")
col3.metric("Modes", "Image · Video · Camera")

st.divider()


# --------------------------------------------------
# Shared result renderer
# --------------------------------------------------

def show_image_result(
    image,
    annotated,
    detections,
    inference_time
):
    annotated = annotated[:, :, ::-1]

    left, right = st.columns(2)

    with left:
        st.subheader("Input")
        st.image(
            image,
            use_container_width=True
        )

    with right:
        st.subheader("Prediction")
        st.image(
            annotated,
            use_container_width=True
        )

    st.divider()

    metric1, metric2 = st.columns(2)

    metric1.metric(
        "Objects Detected",
        len(detections)
    )

    metric2.metric(
        "Inference Time",
        f"{inference_time:.2f} s"
    )

    if detections:

        st.subheader("Detection Summary")

        st.dataframe(
            detections,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No detections found at the selected confidence threshold."
        )


# --------------------------------------------------
# Detection modes
# --------------------------------------------------

image_tab, video_tab, camera_tab = st.tabs(
    [
        "Image Detection",
        "Video Detection",
        "Camera Detection"
    ]
)


# --------------------------------------------------
# Image detection
# --------------------------------------------------

with image_tab:

    st.subheader("Image Inspection")

    st.caption(
        "Upload a workplace image to detect PPE and safety violations."
    )

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )

    if uploaded_image:

        image = Image.open(
            uploaded_image
        ).convert("RGB")

        annotated, detections, inference_time = predict_image(
            model,
            image,
            confidence
        )

        show_image_result(
            image,
            annotated,
            detections,
            inference_time
        )


# --------------------------------------------------
# Video detection
# --------------------------------------------------

with video_tab:

    st.subheader("Video Inspection")

    st.caption(
        "Upload a video for frame-by-frame PPE detection."
    )

    uploaded_video = st.file_uploader(
        "Choose a video",
        type=["mp4", "mov", "avi"],
        key="video_upload"
    )

    if uploaded_video:

        st.video(uploaded_video)

        if st.button(
            "Run Detection",
            type="primary"
        ):

            with st.spinner(
                "Processing video..."
            ):

                output_path = process_video(
                    model,
                    uploaded_video,
                    confidence
                )

            st.success(
                "Video processing complete."
            )

            st.video(
                str(output_path)
            )


# --------------------------------------------------
# Camera detection
# --------------------------------------------------

with camera_tab:

    st.subheader("Camera Inspection")

    st.caption(
        "Capture an image directly from the browser camera."
    )

    camera_image = st.camera_input(
        "Capture image"
    )

    if camera_image:

        image = Image.open(
            camera_image
        ).convert("RGB")

        annotated, detections, inference_time = predict_image(
            model,
            image,
            confidence
        )

        show_image_result(
            image,
            annotated,
            detections,
            inference_time
        )