const tumorInfo = {
  glioma: {
    description:
      "Gliomas are a type of tumor that begins in the glial cells of the brain or spine, which support nerve cells. They vary significantly in severity and can grow quickly. High-grade gliomas are aggressive and require immediate and intensive treatment, while low-grade types grow more slowly and may be monitored or treated less aggressively initially.",
    prescription:
      "Treatment often involves a combination of **surgery** to remove as much of the tumor as safely possible, followed by **radiation therapy** and often **chemotherapy** to target remaining cells. Post-treatment, regular **MRI scans** are critical for monitoring recurrence and treatment effectiveness.",
    prevention:
      "Although there are no guaranteed prevention methods for gliomas, reducing prolonged exposure to **ionizing radiation**, avoiding known **carcinogenic substances**, and maintaining overall brain health through **balanced nutrition** and **stress management** may help reduce general risk.",
    precaution:
      "Patients should actively track **neurological symptoms** like persistent headaches, seizures, and cognitive changes (e.g., memory issues, confusion). **Regular checkups** and diagnostic **imaging** are essential for continuous monitoring, early detection of progression, or recurrence.",
  },

  meningioma: {
    description:
      "Meningiomas develop in the meninges—the protective layers surrounding the brain and spinal cord. Most meningiomas are **benign (non-cancerous)**, but their size and precise location can cause significant pressure effects on brain tissue, leading to symptoms such as vision problems, headaches, or memory loss.",
    prescription:
      "The primary treatment is **surgical removal**. If complete removal isn't possible due to tumor location, or if the tumor recurs, **radiation therapy** is a considered option. Hormonal factors may also influence growth in some cases, which could impact management.",
    prevention:
      "Currently, there are no proven or specific ways to prevent meningiomas. Therefore, **early diagnosis** through regular imaging (especially in symptomatic individuals) is key for timely intervention and better outcomes.",
    precaution:
      "Patients should stay alert to gradual but persistent **neurological changes**. Any new or worsening symptoms, even subtle ones, should prompt a consultation with a neurologist for thorough evaluation and monitoring.",
  },

  notumor: {
    description:
      "Your uploaded brain scan does not show signs of a tumor. The brain structure appears within normal anatomical limits, and no abnormal growths were detected in this analysis. This indicates a healthy scan result.",
    prescription:
      "No specific medical intervention for a tumor is needed. Focus on maintaining your brain and neurological health through a **healthy lifestyle**. Consult a doctor immediately if any new or concerning neurological symptoms arise.",
    prevention:
      "To keep your brain healthy: engage in **regular exercise**, eat a **balanced diet** rich in omega-3 fatty acids and antioxidants, **avoid alcohol and tobacco use**, and prioritize **good sleep hygiene**. These habits support overall brain function.",
    precaution:
      "Stay aware of any persistent symptoms such as unexplained or severe headaches, sudden memory issues, or vision changes. While no tumor is present, **periodic health checkups** are always advised for general wellness and early detection of any health concerns.",
  },

  pituitary: {
    description:
      "Pituitary tumors originate in the pituitary gland, a small but critical endocrine gland at the base of the brain. These tumors can disrupt normal hormone production, potentially affecting growth, metabolism, reproduction, and other vital bodily functions. Some may also press on nearby optic nerves, impairing vision.",
    prescription:
      "Treatment may include **transsphenoidal surgery** (a minimally invasive removal technique), **radiation therapy**, or **lifelong hormone therapy** depending on the specific tumor type and its effects. A comprehensive **endocrinological evaluation** is essential to assess hormone levels and guide treatment.",
    prevention:
      "There are no known preventive measures for pituitary tumors. However, **early detection** through hormone testing and brain imaging is crucial to identify tumors before they cause significant complications or irreversible damage.",
    precaution:
      "Monitor for signs of **hormonal imbalances** (e.g., unexplained fatigue, significant weight changes, menstrual irregularities, infertility, or excessive growth) and **visual disturbances** (e.g., blurred vision, loss of peripheral vision). Seek regular **endocrine checkups** if diagnosed or if these symptoms appear.",
  },
};

// Function to handle prediction and display details
async function predictTumor() {
  const input = document.getElementById("imageInput");
  const resultDiv = document.getElementById("result");
  const loadingDiv = document.getElementById("loading");
  const detailsDiv = document.getElementById("tumorDetails");

  if (!input.files[0]) {
    alert("Please select an image.");
    return;
  }

  const formData = new FormData();
  formData.append("image", input.files[0]);

  resultDiv.innerHTML = "";
  detailsDiv.innerHTML = "";
  loadingDiv.classList.remove("hidden"); // Show loading indicator

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    loadingDiv.classList.add("hidden"); // Hide loading indicator

    if (data.prediction) {
      resultDiv.innerHTML = `✅ <strong>${data.prediction.toUpperCase()}</strong> detected with <strong>${(
        data.confidence * 100
      ).toFixed(2)}%</strong> confidence.`;

      const info = tumorInfo[data.prediction];
      if (info) {
        detailsDiv.innerHTML = `
          <h3>🧾 Details for ${data.prediction.toUpperCase()}</h3>
          <p><strong>Description:</strong> ${info.description}</p>
          <p><strong>Prescription:</strong> ${info.prescription}</p>
          <p><strong>Prevention:</strong> ${info.prevention}</p>
          <p><strong>Precaution:</strong> ${info.precaution}</p>
          <hr style="margin: 15px 0; border-color: #444;" />
          <p style="color:#ff8c00; font-size:0.85em;"><strong>⚠️ Disclaimer:</strong> This result is generated by a machine learning model developed for academic and research purposes. It is not a substitute for professional medical diagnosis. Always consult a certified medical specialist for accurate interpretation and guidance.</p>
        `;
      }
    } else {
      resultDiv.innerHTML = "❌ Prediction failed. Please try another image or ensure it's a valid brain scan.";
    }
  } catch (error) {
    loadingDiv.classList.add("hidden"); // Hide loading indicator on error
    resultDiv.innerHTML = `❌ Error during prediction: ${error.message}. Please check the server connection and try again.`;
  }
}