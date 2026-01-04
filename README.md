♻️ Waste Sorter AI

Waste Sorter AI is a web-based machine learning application that automatically classifies waste images into different categories such as **cardboard, glass, metal, paper, plastic, and trash**.  
The goal of this project is to promote **efficient waste segregation** using AI.

Live Demo:  
https://waste-sorter-ai.onrender.com

---

Features

- Upload an image of waste
- AI-powered waste classification using a trained CNN model
- Displays top predictions with confidence scores
- Generate and download a PDF waste analysis report
- Deployed online using **Render**

---

## Model Details

- **Model Type:** Convolutional Neural Network (CNN)
- **Base Architecture:** MobileNetV2 (pretrained & fine-tuned)
- **Framework:** TensorFlow / Keras
- **Classes:**
  - Cardboard
  - Glass
  - Metal
  - Paper
  - Plastic
  - Trash

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- TensorFlow / Keras
- Gunicorn

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Render (Free Tier)

---

## 📂 Project Structure
Waste-Sorter-AI/
│
├── app.py # Main Flask application
├── utils.py # Model loading & prediction logic
├── model/
│ └── waste_model.h5 # Trained ML model
├── static/
│ ├── css/
│ ├── js/
│ └── uploads/
├── templates/
│ └── index.html
├── requirements.txt
├── Procfile
└── README.md

 ## Screenshots
 ![WhatsApp Image 2026-01-04 at 3 55 11 PM](https://github.com/user-attachments/assets/2b82e027-32a7-42a8-afa4-de261d740392)


