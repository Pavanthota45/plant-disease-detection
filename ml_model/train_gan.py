import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from PIL import Image

# -----------------------
# CONFIG
# -----------------------
IMG_SIZE = 64
LATENT_DIM = 100
EPOCHS = 3000
BATCH_SIZE = 32

# project paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

DATASET_PATH = os.path.join(BASE_DIR, "dataset_small", "train")
GENERATED_PATH = os.path.join(BASE_DIR, "generated")

os.makedirs(GENERATED_PATH, exist_ok=True)

# -----------------------
# LOAD IMAGES
# -----------------------
def load_images():
    images = []
    classes = os.listdir(DATASET_PATH)

    for cls in classes:
        class_folder = os.path.join(DATASET_PATH, cls)

        for file in os.listdir(class_folder):
            try:
                img = Image.open(os.path.join(class_folder, file)).convert("RGB")
                img = img.resize((IMG_SIZE, IMG_SIZE))
                img = np.array(img) / 127.5 - 1.0
                images.append(img)
            except:
                pass

    return np.array(images)

print("Loading dataset...")
X_train = load_images()
print("Total images:", len(X_train))

# -----------------------
# GENERATOR
# -----------------------
def build_generator():
    model = tf.keras.Sequential()

    model.add(layers.Dense(8*8*256, use_bias=False, input_shape=(LATENT_DIM,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((8,8,256)))

    model.add(layers.Conv2DTranspose(128, (5,5), strides=(2,2), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5,5), strides=(2,2), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(3, (5,5), strides=(2,2), padding='same', use_bias=False, activation='tanh'))

    return model

# -----------------------
# DISCRIMINATOR
# -----------------------
def build_discriminator():
    model = tf.keras.Sequential()

    model.add(layers.Conv2D(64, (5,5), strides=(2,2), padding='same',
                            input_shape=(IMG_SIZE,IMG_SIZE,3)))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5,5), strides=(2,2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model

generator = build_generator()
discriminator = build_discriminator()

cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

# -----------------------
# LOSS FUNCTIONS
# -----------------------
def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    return real_loss + fake_loss

def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)

generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

# -----------------------
# TRAIN STEP
# -----------------------
@tf.function
def train_step(images):

    noise = tf.random.normal([BATCH_SIZE, LATENT_DIM])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:

        generated_images = generator(noise, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

    return gen_loss, disc_loss

# -----------------------
# SAVE GENERATED IMAGE
# -----------------------
def save_images(epoch):
    noise = tf.random.normal([1, LATENT_DIM])
    generated_image = generator(noise, training=False)[0]
    generated_image = (generated_image + 1) / 2.0

    img = tf.keras.preprocessing.image.array_to_img(generated_image)
    img.save(os.path.join(GENERATED_PATH, f"generated_{epoch}.png"))

# -----------------------
# TRAIN LOOP
# -----------------------
dataset = tf.data.Dataset.from_tensor_slices(X_train).shuffle(1000).batch(BATCH_SIZE)

print("Starting GAN training...")

for epoch in range(EPOCHS):

    for image_batch in dataset:
        g_loss, d_loss = train_step(image_batch)

    if epoch % 100 == 0:
        print(f"Epoch {epoch} | Gen Loss: {g_loss:.4f} | Disc Loss: {d_loss:.4f}")
        save_images(epoch)

print("GAN Training Complete!")
