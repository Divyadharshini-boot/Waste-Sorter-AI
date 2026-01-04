import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

# -------------------------------
# SETTINGS
# -------------------------------
DATASET_DIR = "archive/dataset-resized"
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 10
MODEL_SAVE_PATH = "model/waste_model.h5"


# -------------------------------
# CHECK PATHS
# -------------------------------
if not os.path.exists(DATASET_DIR):
    print("❌ Dataset folder not found!")
    print("Create a folder named 'dataset' and put class folders inside it.")
    exit()

os.makedirs("model", exist_ok=True)

# -------------------------------
# DATA GENERATOR
# -------------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)
print("Class indices:", train_data.class_indices)


val_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# -------------------------------
# MODEL (MobileNetV2)
# -------------------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

base_model.trainable = False  # freeze base model

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(train_data.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

# -------------------------------
# COMPILE
# -------------------------------
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# -------------------------------
# TRAIN
# -------------------------------
print("🚀 Training started...")
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# -------------------------------
# SAVE MODEL
# -------------------------------
model.save(MODEL_SAVE_PATH)
print(f"✅ Model saved at {MODEL_SAVE_PATH}")
