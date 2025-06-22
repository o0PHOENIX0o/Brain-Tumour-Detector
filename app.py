import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load the trained model
model = tf.keras.models.load_model("brain_model.h5")

# Class names - update based on your dataset folder names
class_names = ['glioma', 'meningioma', 'notumor', 'pituitary']

# Tumor details dictionary
tumor_info = {
    "glioma": {
        "description": "Gliomas are tumors that originate in the glial cells of the brain or spine. They are often aggressive and may affect brain function.",
        "prescription": "Treatment may include surgery, radiation therapy, chemotherapy (e.g., temozolomide), and targeted drug therapy. Regular MRI scans and follow-ups are essential.",
        "prevention": "While not entirely preventable, reducing radiation exposure and avoiding carcinogens may lower risk. Healthy lifestyle and early diagnosis improve outcomes."
    },
    "meningioma": {
        "description": "Meningiomas arise from the meninges, the membranes that surround the brain and spinal cord. Most are benign but can grow and press on brain tissue.",
        "prescription": "Often treated with surgical removal. Radiation therapy may be used if surgery isn’t an option or the tumor is not fully removed.",
        "prevention": "There is no known prevention, but early imaging if symptoms arise (e.g., headaches, vision problems) can help in timely intervention."
    },
    "notumor": {
        "description": "No brain tumor detected in the MRI scan. The brain appears structurally normal.",
        "prescription": "No medical intervention required. Maintain regular health checkups and consult a neurologist if symptoms persist.",
        "prevention": "Follow a brain-healthy lifestyle: avoid smoking, limit alcohol, exercise regularly, eat a balanced diet, and manage stress."
    },
    "pituitary": {
        "description": "Pituitary tumors form in the pituitary gland. They can affect hormone production and cause vision issues due to proximity to the optic nerve.",
        "prescription": "Treatment includes medication (e.g., dopamine agonists), surgery (transsphenoidal resection), and radiation. Hormone replacement may be necessary.",
        "prevention": "Most pituitary tumors aren’t preventable. Early detection and endocrine evaluation are key for effective treatment."
    }
}

# App title
st.title("🧠 Brain Tumor Detection")
st.markdown("Upload a brain MRI scan and the model will predict the type of tumor.")

# Upload image
uploaded_file = st.file_uploader("Choose a brain MRI image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_container_width=True)

    # Preprocess the image
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    confidence = 100 * np.max(prediction)

    # Show prediction
    st.success(f"🧾 Prediction: **{predicted_class.upper()}** ({confidence:.2f}% confidence)")

    # If a tumor is detected (not "notumor"), show urgent medical advice
    if predicted_class != "notumor":
        st.error("⚠️ Tumor detected! Please consult a neurologist or oncologist **immediately** for further diagnosis and treatment.")

    # Show tumor details
    info = tumor_info[predicted_class]
    
    st.subheader("📋 Medical Description:")
    st.write(info["description"])

    st.subheader("💊 Prescription:")
    st.write(info["prescription"])

    st.subheader("🛡️ Prevention Tips:")
    st.write(info["prevention"])
