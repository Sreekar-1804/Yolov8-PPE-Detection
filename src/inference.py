import time


def predict_image(model, image, confidence=0.25):

    start = time.perf_counter()

    result = model.predict(
        source=image,
        conf=confidence,
        verbose=False
    )[0]

    inference_time = time.perf_counter() - start

    annotated = result.plot()

    detections = []

    if result.boxes is not None:

        for box in result.boxes:

            class_id = int(box.cls[0])
            score = float(box.conf[0])

            detections.append(
                {
                    "class": result.names[class_id],
                    "confidence": round(score, 3)
                }
            )

    return annotated, detections, inference_time


def predict_frame(model, frame, confidence=0.25):

    result = model.predict(
        source=frame,
        conf=confidence,
        verbose=False
    )[0]

    return result.plot()