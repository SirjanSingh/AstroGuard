#  Space Station Object Detector

**Team:** Ctrl+Alt+Elite  
**Members:** Ritigya Gupta, Sirjan Singh, Manasvi Methi, Heeral Mandolia  
**Hackathon:** Duality AI - Space Station Hackathon  
**Theme:** Object Detection in Simulated Space Environments

---

##  Problem Statement

In the high-risk environment of a space station, it’s crucial to detect essential tools like fire extinguishers, oxygen tanks, and toolboxes in real time to ensure crew safety and mission efficiency.

---

##  Objective

Develop a **fast, lightweight, and accurate object detection model** capable of identifying critical equipment from space station surveillance feeds.

---

##  Approach

We built our detection pipeline using **YOLOv8** and focused on the following object classes:

- 🧯 Fire Extinguisher  
- 🧰 Toolbox  
- 🛢️ Oxygen Tank  

---

##  Model Development Process

We went through several iterations to find the most optimal configuration for both accuracy and generalization:

### 1.  YOLOv8s (Small) – 40 Epochs (Best Model)
- Best model with balanced performance  
- Fast inference and high accuracy  
- Chosen as the final model for submission

### 2. YOLOv8m (Medium) – 50 Epochs
- Improved training metrics (lower loss, higher precision)  
- **But**: Test performance began to fluctuate (overfitting symptoms)

### 3.  YOLOv8s – 50 Epochs (`train10`)
- Stable metrics  
- Comparable to final model but slightly heavier

### 4.  YOLOv8m – 50 Epochs (`train7`)
- More complex model  
- Slight overfitting observed

---

##  Training Comparison Summary

| Model          | Epochs | Type | Overall | FireExt. | ToolBox | OxyTank |
|----------------|--------|------|---------|----------|---------|---------|
| `train5`       | 40     | s    | 87.9    | 88.9     | 87.7    | 87.1    |
| `train4`       | ?      | s    | 86.75   | 75.51    | 81.24   | 76.03   |
| `train10`      | 50     | s    | 86.68   | 76.07    | 81.34   | 76.18   |
| `train7`       | 50     | m    | 86.68   | 76.07    | 81.34   | 76.18   |
| `train_5epochs`| 5      | s    | 71.79   | 62.77    | 60.51   | 48.96   |

 Based on overall performance and generalization, **`train5` (YOLOv8s – 40 Epochs)** was selected as the **final model**.

---

##  Final Evaluation Metrics

Tested on 400 unseen images:

| Metric                            | Value             |
| --------------------------------- | ----------------- |
| **mAP\@0.5**                      | **87.9%**         |
| **mAP\@0.5:0.95**                 | **78.1%**         |
| **Precision (P)**                 | **95.0%**         |
| **Recall (R)**                    | **79.7%**         |
| **Inference Time**                | **5.8 ms/image**  |
| **Preprocess + Postprocess Time** | **0.6ms + 2.6ms** |


---

##  Class-Wise Performance

| Class             | Precision (P) | Recall (R) | mAP\@0.5 | mAP\@0.5:0.95 |
| ----------------- | ------------- | ---------- | -------- | ------------- |
| Fire Extinguisher | 95.9%         | 82.0%      | 88.9%    | 76.7%         |
| Toolbox           | 95.0%         | 79.3%      | 87.7%    | 80.4%         |
| Oxygen Tank       | 94.1%         | 77.7%      | 87.1%    | 77.1%         |


-  Confusion Matrix showed minor confusion with background (typical for cluttered space scenes)  
-  F1-Confidence Curve peaked at confidence ≈ **0.598** (recommended threshold)

---

##  Dataset Summary

- Structured in YOLO format (`.txt` labels)  
- Verified 100% consistency between images and labels  
- Simulated dataset with realistic lighting, positioning, and occlusions inside a space station

---

##  Tech Stack

- **YOLOv8** (Ultralytics)  
- **Python**  
- **OpenCV** – Image processing  
- **PyYAML** – Configuration handling  
- **Tkinter** – GUI for model predictions  
- **Google Colab** – GPU training on Tesla T4

---

##  How to Run the Project

###  Run Streamlit App

bash
streamlit run app.py

###  Run Tkinter GUI
cd tkinter
python app.py

---
#  Screenshots
This section contains all the screenshots and visual outputs of our application


![image](https://github.com/user-attachments/assets/aa0109b1-6752-427b-a565-392da22e1b23)
![image](https://github.com/user-attachments/assets/8827521f-adc5-4a7c-abc5-0b56f6b08c28)
![image](https://github.com/user-attachments/assets/f5ad1346-9a35-4c74-85b6-41d4226a9173)
