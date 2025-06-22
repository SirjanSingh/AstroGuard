# 🚀 Space Station Object Detector

**Team:** Ctrl+Alt+Elite  
**Members:** Ritigya Gupta, Sirjan Singh, Manasvi Methi, Heeral Mandolia  
**Hackathon:** Duality AI - Space Station Hackathon  
**Theme:** Object Detection in Simulated Space Environments
---

## 🧩 Problem Statement

In the high-risk environment of a space station, it’s crucial to detect essential tools like fire extinguishers, oxygen tanks, and toolboxes in real time to ensure crew safety and mission efficiency.

---

## 🎯 Objective

Develop a **fast, lightweight, and accurate object detection model** capable of identifying critical equipment from space station surveillance feeds.

---

## 🧠 Approach

We built our detection pipeline using **YOLOv8** and focused on the following object classes:
- 🧯 Fire Extinguisher
- 🧰 Toolbox
- 🛢️ Oxygen Tank

---

## ⚙️ Model Development Process

We went through several iterations to find the most optimal configuration for both accuracy and generalization:

### 1. **YOLOv8s (Small) - 30 Epochs** 
- Initial training run
- Achieved high accuracy
- **mAP@0.5**: 93.2% | **Precision**: 92.7% | **Recall**: 91.2%

### 1. **YOLOv8s (Small) – 40 Epochs**
- Initial successful training run
- Fast inference and high accuracy
- **mAP@0.5**: 94.6% | **Precision**: 98.7% | **Recall**: 91.2%

### 2. **YOLOv8m (Medium) – 50 Epochs**
- Improved training metrics (lower loss, higher precision)
- **But**: Test performance began to fluctuate (overfitting symptoms)

### 3. ✅ **YOLOv8s – 50 Epochs (Final Model)**
- Balanced performance across training and testing
- No overfitting observed
- Chosen as the **final model** for submission

---

## 📊 Final Evaluation Metrics

Tested on 400 unseen images:

| Metric         | Value     |
|----------------|-----------|
| **mAP@0.5**     | 94.6%     |
| **mAP@0.5:0.95**| 88.9%     |
| **Precision**   | 98.7%     |
| **Recall**      | 91.2%     |
| **Inference**   | ~11ms/img |

---

## 📈 Class-Wise Performance

| Class             | AP@0.5 |
|-------------------|--------|
| Fire Extinguisher | 0.975  |
| Toolbox           | 0.937  |
| Oxygen Tank       | 0.944  |
| **Overall mAP**   | **0.952** |

- **Confusion Matrix** showed minor confusion with background (typical for cluttered space scenes)
- **F1-Confidence Curve** peaked at confidence ≈ 0.598 (suggested threshold)

---

## 🔍 Dataset Summary

- Structured in YOLO format (`.txt` labels)
- Verified 100% consistency between images and labels
- Simulated dataset with realistic lighting, positioning, and occlusions inside a space station

---

## 🛠️ Tech Stack


- **YOLOv8** (Ultralytics)
- **Python**
- **OpenCV** – image processing
- **PyYAML** – configuration handling
- **Tkinter** – GUI integration for predictions
- **Google Colab** – GPU training on Tesla T4
---