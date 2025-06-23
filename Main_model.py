import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.metrics import Precision, Recall
import matplotlib.pyplot as plt
import os

# === Data Preprocessing ===
train_datagen = ImageDataGenerator(
    rescale=1./255,
    zoom_range=0.5,
    rotation_range=15,
    shear_range=0.5,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

img_size = (224, 224)
batch_size = 32


train_data = train_datagen.flow_from_directory(
    r"C:\Users\Krish Sharma\Desktop\programming\python\AI Course Udemy\Neural Networks\ANN Project Implementation\Brain Tumour Detection Using Cnn\archive (1)\Brain Tumor Data(1)\Brain Tumor Data\Brain Tumor data\Brain Tumor data\Training",
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

test_data = test_datagen.flow_from_directory(
    r"C:\Users\Krish Sharma\Desktop\programming\python\AI Course Udemy\Neural Networks\ANN Project Implementation\Brain Tumour Detection Using Cnn\archive (1)\Brain Tumor Data(1)\Brain Tumor Data\Brain Tumor data\Brain Tumor data\Testing",
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)


# === Model Definition ===
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax')
])

model.summary()

# === Compile Model ===
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy', Precision(name="precision"), Recall(name="recall")]
)

# === Train Model ===
history = model.fit(
    train_data,
    epochs=15,
    validation_data=test_data
)

# === Plot Accuracy ===
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.grid()
plt.show()

# === Plot Loss ===
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid()
plt.show()

# === Evaluate Model ===
loss, accuracy, precision, recall = model.evaluate(test_data)
print(f"Test Accuracy  : {accuracy * 100:.2f}%")
print(f"Test Precision : {precision * 100:.2f}%")
print(f"Test Recall    : {recall * 100:.2f}%")

# === Save Model ===
model.save("brain_tumor_customize_model.h5")
