import os
import random
import time
from fpdf import FPDF
from PIL import Image

# Classes for Waste Classification
CLASSES = ['Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic', 'Trash']

class ModelHandler:
    def __init__(self):
        self.model = None
        # In a real scenario, we would load the model here:
        # self.model = tf.keras.models.load_model('model/waste_classifier.h5')
        print("Model initialized (Demo Mode)")

    def predict(self, image_path):
        """
        Simulates prediction since we don't have the specific WasteNet weights.
        In production, you would:
        1. Load image using PIL or cv2
        2. Preprocess (resize, normalize)
        3. Run self.model.predict()
        """
        # Simulate processing time
        time.sleep(1)
        
        # Generate random confidence scores for demo purposes
        # In a real app, these would come from the model
        scores = [random.random() for _ in range(len(CLASSES))]
        total = sum(scores)
        normalized_scores = [s/total * 100 for s in scores]
        
        # Create list of (class, score) tuples and sort by score
        results = list(zip(CLASSES, normalized_scores))
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Format top 3 for output
        top_3 = [
            {'label': label, 'confidence': round(score, 2)}
            for label, score in results[:3]
        ]
        
        return top_3

def generate_pdf_report(image_path, predictions):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 20, "Waste Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    # Image
    # Ensure image fits in the page
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
