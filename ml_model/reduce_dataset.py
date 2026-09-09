import os
import shutil
import random

# Get project root automatically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCE_DIR = os.path.join(BASE_DIR, "dataset", "train")
DEST_DIR = os.path.join(BASE_DIR, "dataset_small", "train")

IMAGES_PER_CLASS = 10

def create_small_dataset():

    if not os.path.exists(SOURCE_DIR):
        print("❌ SOURCE DATASET NOT FOUND:", SOURCE_DIR)
        return

    os.makedirs(DEST_DIR, exist_ok=True)

    classes = os.listdir(SOURCE_DIR)

    for cls in classes:
        class_src = os.path.join(SOURCE_DIR, cls)
        class_dst = os.path.join(DEST_DIR, cls)

        if not os.path.isdir(class_src):
            continue

        os.makedirs(class_dst, exist_ok=True)

        images = os.listdir(class_src)

        if len(images) == 0:
            continue

        selected_images = random.sample(images, min(IMAGES_PER_CLASS, len(images)))

        for img in selected_images:
            shutil.copy(
                os.path.join(class_src, img),
                os.path.join(class_dst, img)
            )

        print(f"Copied {len(selected_images)} images -> {cls}")

    print("\n✅ SMALL DATASET READY!")

if __name__ == "__main__":
    create_small_dataset()