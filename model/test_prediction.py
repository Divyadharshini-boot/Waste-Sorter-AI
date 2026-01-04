from utils import ModelHandler

# Initialize the model
model = ModelHandler()

# Path to an image you want to test
# Replace with any real image from your dataset
image_path = 'C:\Users\divya\Downloads\Waste-Sorter-AI\Waste-Sorter-AI\archive\dataset-resized\paper\paper6.jpg'

# Get predictions
predictions = model.predict(image_path)

# Print the results
print("Top 3 predictions:")
for i, pred in enumerate(predictions, 1):
    print(f"{i}. {pred['label']} - {pred['confidence']}%")
