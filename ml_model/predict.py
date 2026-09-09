import tensorflow as tf
import numpy as np
import os
from PIL import Image, ImageOps

# ===== Paths =====
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "model.h5")
DATASET_PATH = os.path.join(BASE_DIR, "dataset_small", "train")

# ===== Load Model =====
model = tf.keras.models.load_model(MODEL_PATH)

# Keep the label order identical to Keras' flow_from_directory ordering.
class_names = sorted(
    name for name in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, name))
)

if model.output_shape[-1] != len(class_names):
    raise ValueError(
        f"Model has {model.output_shape[-1]} outputs, but the dataset has "
        f"{len(class_names)} class folders. Retrain the model with this dataset."
    )

IMAGE_SIZE = tuple(model.input_shape[1:3])

def predict_disease(image_path):

    img = ImageOps.exif_transpose(Image.open(image_path)).convert("RGB")
    img = img.resize(IMAGE_SIZE)
    img = np.asarray(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img,axis=0)

    prediction = model.predict(img, verbose=0)

    index = int(np.argmax(prediction[0]))
    confidence = float(np.max(prediction))

    disease_name = class_names[index]

    # Clean label for display
    disease_name = disease_name.replace("___"," - ").replace("_"," ")

    return disease_name, confidence