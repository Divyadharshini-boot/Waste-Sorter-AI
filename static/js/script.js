let currentStream = null;
let lastAnalysisData = null;

// File Upload Handling
document.getElementById('fileInput').addEventListener('change', handleFileSelect);
document.getElementById('dropZone').addEventListener('click', () => document.getElementById('fileInput').click());

document.getElementById('dropZone').addEventListener('dragover', (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('bg-white');
});

document.getElementById('dropZone').addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('bg-white');
});

document.getElementById('dropZone').addEventListener('drop', (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('bg-white');
    const files = e.dataTransfer.files;
    if (files.length) uploadFile(files[0]);
});

function handleFileSelect(e) {
    if (e.target.files.length) uploadFile(e.target.files[0]);
}

// Camera Handling
async function startCamera() {
    try {
        const video = document.getElementById('video');
        currentStream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = currentStream;
    } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Could not access camera. Please ensure you have given permission.");
    }
}

document.getElementById('captureBtn').addEventListener('click', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    canvas.toBlob(blob => {
        const file = new File([blob], "camera_capture.jpg", { type: "image/jpeg" });
        uploadFile(file);
    }, 'image/jpeg');
    
    // Stop camera
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
    }
});

// Upload and Analyze
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show Preview
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('imagePreview').src = e.target.result;
        document.getElementById('previewSection').classList.remove('d-none');
        document.getElementById('loadingSpinner').classList.remove('d-none');
        document.getElementById('resultsSection').classList.add('d-none');
    };
    reader.readAsDataURL(file);
    
    // API Call
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').classList.add('d-none');
        if (data.success) {
            displayResults(data);
        } else {
            alert('Analysis failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loadingSpinner').classList.add('d-none');
        alert('An error occurred during analysis.');
    });
}

function displayResults(data) {
    lastAnalysisData = data;
    const results = document.getElementById('resultsSection');
    const list = document.getElementById('predictionsList');
    
    // Main Result
    const top = data.predictions[0];
    document.getElementById('mainLabel').textContent = top.label;
    document.getElementById('mainScore').textContent = top.confidence + '%';
    
    // List
    list.innerHTML = data.predictions.map(p => `
        <div class="list-group-item d-flex justify-content-between align-items-center">
            ${p.label}
            <span class="badge bg-primary rounded-pill">${p.confidence}%</span>
        </div>
    `).join('');
    
    results.classList.remove('d-none');
    results.scrollIntoView({ behavior: 'smooth' });
}

function downloadReport() {
    if (!lastAnalysisData) return;
    
    fetch('/report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(lastAnalysisData)
    })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'EcoSort_Report.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
}
