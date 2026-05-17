import cv2

backends = [
    ("DEFAULT", 0),
    ("DSHOW", cv2.CAP_DSHOW),
    ("MSMF", cv2.CAP_MSMF),
]

for backend_name, backend in backends:
    print("\nTesting backend:", backend_name)

    if backend_name == "DEFAULT":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(0, backend)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    for _ in range(20):
        ret, frame = cap.read()

    print("Opened:", cap.isOpened())
    print("Frame read:", ret)
    print("Frame shape:", None if frame is None else frame.shape)
    print("Mean pixel:", None if frame is None else frame.mean())

    cap.release()