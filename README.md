<div align="center">

# 🚀 DeskDetect — YOLOv8 Custom Object Detection

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-10b981.svg)](https://github.com/ultralytics/ultralytics)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c.svg)](https://pytorch.org/)
[![Gradio](https://img.shields.io/badge/Gradio-Web%20App-orange.svg)](https://gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


</div>

---

## 📌 About the Project
**DeskDetect** explores the complete workflow of a modern computer vision pipeline. Built using **YOLOv8** and trained on a custom subset of the **COCO 2017** dataset via **Google Colab (T4 GPU)**, the model accurately detects everyday desktop and workspace objects through an interactive, dark-themed **Gradio web interface**.

---

## 🎯 Selected Classes & Dataset Distribution
The model was trained on 5 core workspace and daily-life categories:
1. `laptop` (955 instances)
2. `keyboard` (578 instances)
3. `mouse` (444 instances)
4. `cell phone` (1,296 instances)
5. `bottle` (4,285 instances)

---

## 📊 Model Performance & Evaluation
| Category / Class | Instances | mAP50 | Status |
| :--- | :---: | :---: | :---: |
| **laptop** | 955 | **0.741** | 🟢 High Precision |
| **cell phone** | 1,296 | **0.682** | 🟢 Good |
| **mouse** | 444 | **0.582** | 🟡 Moderate |
| **keyboard** | 578 | **0.548** | 🟡 Moderate |
| **bottle** | 4,285 | **0.536** | 🟡 Moderate |
| **Overall (all)** | **7,558** | **0.578** | **Solid Baseline** |

- **Precision:** 70.1% accuracy on positive detections.
- **Model Checkpoint:** Saved as `best.pt` in the repository root.

---

## 🛠️ Quick Start & Installation
To run the web interface locally on your machine without Google Colab:

### 1. Clone the Repository
```bash
git clone [https://github.com/beyzacolaklar/yolo.git](https://github.com/beyzacolaklar/yolo.git)
cd yolo
