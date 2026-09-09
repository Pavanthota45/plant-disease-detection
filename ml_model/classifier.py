import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

# ===== Automatically find project root =====
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

# ===== Use SMALL dataset =====
dataset_path = os.path.join(BASE_DIR, "dataset_small", "train")

print("Dataset path used:", dataset_path)

IMG_SIZE = 128

train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=(0.8, 1.2)
)

val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=16,
    class_mode='categorical',
    subset='training'
)

val_data = val_datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=16,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

class_counts = np.bincount(train_data.classes, minlength=train_data.num_classes)
class_weights = {
    class_id: len(train_data.classes) / (train_data.num_classes * count)
    for class_id, count in enumerate(class_counts)
    if count > 0
}

# ===== CNN Model =====
model = models.Sequential([
    tf.keras.Input(shape=(128,128,3)),
    layers.Conv2D(32,(3,3),activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128,(3,3),activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128,activation='relu'),
    layers.Dense(train_data.num_classes,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nTraining started...\n")

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=20,
    class_weight=class_weights
)

# ===== Save Model =====
model_save_path = os.path.join(BASE_DIR, "ml_model", "model.h5")
model.save(model_save_path)

print("\n✅ MODEL TRAINED SUCCESSFULLY")
print("Model saved at:", model_save_path)