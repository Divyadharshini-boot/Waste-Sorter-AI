import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from utils import ModelHandler, generate_pdf_report

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Model
model_handler = ModelHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get predictions
        predictions = model_handler.predict(filepath)
        
        return jsonify({
            'success': True,
            'image_url': url_for('static', filename=f'uploads/{filename}'),
            'predictions': predictions
        })

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    image_path = os.path.join(app.root_path, data['image_url'].lstrip('/'))
    predictions = data['predictions']
    
    pdf_path = generate_pdf_report(image_path, predictions)
    return send_file(pdf_path, as_attachment=True, download_name='waste_analysis_report.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
