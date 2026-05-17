# 📌 Real-Time PPE Detection using YOLOv8

## 🔍 Overview

This project implements a computer vision pipeline for detecting Personal Protective Equipment (PPE) such as **hardhats** and **safety vests** using Ultralytics YOLOv8.

The system is designed as a prototype for workplace safety monitoring, capable of detecting whether individuals are compliant with safety requirements in images, videos, and real-time webcam streams.

---

## 🎯 Problem Statement

In industrial and construction environments, ensuring that workers wear appropriate safety equipment is critical. Manual monitoring is not scalable and prone to errors.

This project explores how object detection can be used to automate PPE compliance monitoring.

---

## 🧠 Approach

* Used a pre-annotated PPE dataset in YOLO format
* Refined the dataset from 14 classes to 5 relevant classes:

  * Hardhat
  * Safety Vest
  * NO-Hardhat
  * NO-Safety Vest
  * Person
* Applied transfer learning using pretrained YOLOv8 weights
* Trained and evaluated the model using standard detection metrics
* Tested the model on:

  * images
  * video input
  * real-time webcam feed

---

## 🛠️ Tech Stack

* Python
* Ultralytics YOLOv8
* OpenCV
* PyTorch
* Jupyter Notebook

---

## 📂 Project Structure

```
yolo-ppe-detection/
├── dataset/                # Original dataset
├── dataset_filtered/       # Refined dataset (selected classes)
├── notebooks/              # Jupyter notebook with full workflow
├── videos/                 # Test videos
├── runs/                   # Training and inference outputs
├── README.md
```

---

## 📊 Model Training

* Model: YOLOv8 Nano (yolov8n)
* Training approach: Transfer Learning
* Input size: 640
* Initial epochs: 10 (for experimentation)

---

## 📈 Evaluation Metrics

The model was evaluated using:

* Precision
* Recall
* mAP@50
* mAP@50-95

These metrics provide insight into detection accuracy and generalization performance.

---

## 🎥 Inference Results

The trained model was tested on:

### 🖼️ Images

* Successfully detected multiple PPE elements
* Handled multiple objects per frame

### 🎬 Video

* Demonstrated consistent detection across frames
* Showed robustness in dynamic scenes

### 📷 Real-Time Webcam

* Implemented real-time detection pipeline
* Achieved near real-time performance (~60 ms per frame)

---

## ⚠️ Limitations

* Limited training epochs (initial experiment)
* Performance may drop under:

  * poor lighting
  * occlusion
  * low-resolution inputs
* Dataset quality impacts detection accuracy

---

## 🚀 Future Improvements

* Train with more epochs for better convergence
* Use larger models (YOLOv8s / YOLOv8m)
* Apply data augmentation
* Optimize for edge deployment
* Integrate with alert/monitoring systems

---

## 💡 Key Learnings

* End-to-end object detection pipeline development
* Dataset preprocessing and class refinement
* Transfer learning for computer vision
* Model evaluation using detection metrics
* Real-time inference implementation

---

## 🧑‍💻 Author

**Naga Sai Satya Sreekar Vanka**
📍 Germany

* LinkedIn: https://www.linkedin.com/in/sreekar-v/
* GitHub: https://github.com/Sreekar-1804
