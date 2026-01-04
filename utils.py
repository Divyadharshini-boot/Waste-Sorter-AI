import os
import time
import numpy as np
from fpdf import FPDF
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Correct class order matching training
CLASSES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

class ModelHandler:
    def __init__(self):
        self.model = load_model('model/waste_model.h5')
        print("✅ Real model loaded")

    def predict(self, image_path):
        # Load image
        img = image.load_img(image_path, target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Get prediction probabilities
        preds = self.model.predict(img_array)[0]

        # Top-3 predictions
        top_idx = np.argsort(preds)[::-1][:3]
        top_preds = [
            {'label': CLASSES[i], 'confidence': round(float(preds[i]*100), 2)}
            for i in top_idx
        ]

        # Simulate processing time (optional)
        time.sleep(0.5)
        return top_preds

def generate_pdf_report(image_path, predictions):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 20, "Waste Analysis Report", ln=True, align='C')
    pdf.ln(10)

    # Image
    pdf.image(image_path, x=60, w=90)
    pdf.ln(10)

    # Results Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Classification Results:", ln=True)
    pdf.ln(5)

    # Predictions
    pdf.set_font("Arial", '', 14)
    for i, pred in enumerate(predictions, 1):
        color = (0, 100, 0) if i == 1 else (0, 0, 0)
        pdf.set_text_color(*color)
        pdf.cell(0, 10, f"{i}. {pred['label']}: {pred['confidence']}%", ln=True)

    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f"Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}", align='R')

    report_path = 'static/uploads/report.pdf'
    pdf.output(report_path)
    return report_path
