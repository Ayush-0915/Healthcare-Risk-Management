import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Risk Prediction",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# -------------------------------------------------
# Load Model & Encoders
# -------------------------------------------------
@st.cache_resource
def load_resources():
    model = joblib.load(DATA_DIR / "risk_prediction_model.pkl")
    label_encoders = joblib.load(DATA_DIR / "label_encoders.pkl")
    target_encoder = joblib.load(DATA_DIR / "target_encoder.pkl")
    df = pd.read_csv(DATA_DIR / "cleaned_healthcare_dataset.csv")
    return model, label_encoders, target_encoder, df


model, label_encoders, target_encoder, df = load_resources()

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🤖 AI Healthcare Risk Prediction")
st.markdown(
    "Enter patient details below and predict the **Risk Category** using the trained machine learning model."
)

st.divider()

# -------------------------------------------------
# Input Form
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=45
    )

    gender = st.selectbox(
        "Gender",
        sorted(df["Gender"].unique())
    )

    blood = st.selectbox(
        "Blood Type",
        sorted(df["Blood Type"].unique())
    )

    admission = st.selectbox(
        "Admission Type",
        sorted(df["Admission Type"].unique())
    )

with col2:
    condition = st.selectbox(
        "Medical Condition",
        sorted(df["Medical Condition"].unique())
    )

    medication = st.selectbox(
        "Medication",
        sorted(df["Medication"].unique())
    )

    test_result = st.selectbox(
        "Test Result",
        sorted(df["Test Results"].unique())
    )

    stay = st.slider(
        "Length of Stay (Days)",
        1,
        30,
        7
    )

# -------------------------------------------------
# Prediction
# -------------------------------------------------
if st.button("🚀 Predict Risk", use_container_width=True):

    input_data = pd.DataFrame({
        "Age": [age],
        "Gender": [gender],
        "Blood Type": [blood],
        "Medical Condition": [condition],
        "Admission Type": [admission],
        "Medication": [medication],
        "Test Results": [test_result],
        "Length of Stay": [stay]
    })

    # Encode categorical values
    for col in [
        "Gender",
        "Blood Type",
        "Medical Condition",
        "Admission Type",
        "Medication",
        "Test Results"
    ]:
        input_data[col] = label_encoders[col].transform(input_data[col])

    # Predict
    prediction = model.predict(input_data)[0]
    risk = target_encoder.inverse_transform([prediction])[0]

    # Probability (if supported)
    confidence = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_data)[0]
        confidence = probs.max() * 100

    st.divider()

    st.subheader("🎯 Prediction Result")

    if risk == "Low":
        st.success(f"✅ Predicted Risk: **{risk}**")
    elif risk == "Medium":
        st.info(f"🟡 Predicted Risk: **{risk}**")
    elif risk == "High":
        st.warning(f"🟠 Predicted Risk: **{risk}**")
    else:
        st.error(f"🔴 Predicted Risk: **{risk}**")

    if confidence is not None:
        st.metric("Model Confidence", f"{confidence:.2f}%")

    st.markdown("### 💡 Recommendation")

    if risk == "Low":
        st.write("- Continue routine monitoring.")
        st.write("- Maintain standard care procedures.")
    elif risk == "Medium":
        st.write("- Increase observation frequency.")
        st.write("- Review patient condition regularly.")
    elif risk == "High":
        st.write("- Prioritize medical attention.")
        st.write("- Schedule additional diagnostic tests.")
    else:
        st.write("- Immediate intervention recommended.")
        st.write("- Notify senior medical staff.")
        st.write("- Continuous monitoring advised.")