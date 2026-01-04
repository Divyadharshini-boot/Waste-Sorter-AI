from utils import ModelHandler

# Initialize the model
model = ModelHandler()


image_path = r'C:\Users\divya\Downloads\archive\dataset-resized\paper\paper6.jpg'



# Get predictions
predictions = model.predict(image_path)

# Print the results
print("Top 3 predictions:")
for i, pred in enumerate(predictions, 1):
    print(f"{i}. {pred['label']} - {pred['confidence']}%")
