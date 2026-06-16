import streamlit as st
import pandas as pd
import joblib
import textwrap
from pathlib import Path

from components.theme import load_css
from components.cards import kpi_card
from components.footer import show_footer
from components.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
logo_path = BASE_DIR / "assets" / "logo.png"

st.set_page_config(
    page_title="AI Risk Prediction",
    page_icon=str(logo_path),
    layout="wide"
)

load_css()

# --------------------------------------------------
# Sidebar & Navigation
# --------------------------------------------------
render_sidebar()

# --------------------------------------------------
# Load Resources
# --------------------------------------------------
@st.cache_resource
def load_resources():
    model = joblib.load(DATA_DIR / "risk_prediction_model.pkl")
    label_encoders = joblib.load(DATA_DIR / "label_encoders.pkl")
    target_encoder = joblib.load(DATA_DIR / "target_encoder.pkl")
    dataset = pd.read_csv(DATA_DIR / "cleaned_healthcare_dataset.csv")
    return model, label_encoders, target_encoder, dataset


try:
    model, label_encoders, target_encoder, df = load_resources()
except Exception as e:
    st.error(f"❌ Failed to load model or dataset.\n\n{e}")
    st.stop()

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🤖 AI Healthcare Risk Prediction")
st.markdown(
    textwrap.dedent(
        """
        Predict the **Risk Category** of a patient using the trained
        Machine Learning model based on demographic and clinical data.
        """
    )
)

# --------------------------------------------------
# Input Form
# --------------------------------------------------
with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 0, 100, 45)

        gender = st.selectbox(
            "Gender",
            sorted(df["Gender"].dropna().unique())
        )

        blood_type = st.selectbox(
            "Blood Type",
            sorted(df["Blood Type"].dropna().unique())
        )

        admission_type = st.selectbox(
            "Admission Type",
            sorted(df["Admission Type"].dropna().unique())
        )

    with col2:

        medical_condition = st.selectbox(
            "Medical Condition",
            sorted(df["Medical Condition"].dropna().unique())
        )

        medication = st.selectbox(
            "Medication",
            sorted(df["Medication"].dropna().unique())
        )

        test_result = st.selectbox(
            "Test Results",
            sorted(df["Test Results"].dropna().unique())
        )

        length_of_stay = st.slider(
            "Length of Stay (Days)",
            1,
            30,
            7
        )

    predict_button = st.form_submit_button(
        "🚀 Predict Risk"
    )

# --------------------------------------------------
# Prediction
# --------------------------------------------------
if predict_button:

    input_df = pd.DataFrame({
        "Age": [age],
        "Gender": [gender],
        "Blood Type": [blood_type],
        "Medical Condition": [medical_condition],
        "Admission Type": [admission_type],
        "Medication": [medication],
        "Test Results": [test_result],
        "Length of Stay": [length_of_stay]
    })

    categorical_cols = [
        "Gender",
        "Blood Type",
        "Medical Condition",
        "Admission Type",
        "Medication",
        "Test Results"
    ]

    try:
        for col in categorical_cols:
            input_df[col] = label_encoders[col].transform(
                input_df[col]
            )

        prediction = model.predict(input_df)[0]

        predicted_risk = target_encoder.inverse_transform(
            [prediction]
        )[0]

        confidence = None

        if hasattr(model, "predict_proba"):
            confidence = (
                model.predict_proba(input_df)[0].max() * 100
            )

        st.divider()

        st.subheader("🎯 Prediction Result")

        if predicted_risk == "Low":
            st.success(f"🟢 Risk Category: **{predicted_risk}**")
            color = "#22c55e"

        elif predicted_risk == "Medium":
            st.info(f"🟡 Risk Category: **{predicted_risk}**")
            color = "#eab308"

        elif predicted_risk == "High":
            st.warning(f"🟠 Risk Category: **{predicted_risk}**")
            color = "#f97316"

        else:
            st.error(f"🔴 Risk Category: **{predicted_risk}**")
            color = "#ef4444"

        c1, c2 = st.columns(2)

        with c1:
            kpi_card(
                title="Predicted Risk",
                value=predicted_risk,
                icon="🩺",
                subtitle="Machine Learning Output",
                color=color
            )

        with c2:
            if confidence is not None:
                kpi_card(
                    title="Model Confidence",
                    value=f"{confidence:.1f}%",
                    icon="🎯",
                    subtitle="Prediction Confidence",
                    color="#3b82f6"
                )

        st.markdown("## 💡 Clinical Recommendation")

        if predicted_risk == "Low":
            st.success(
                textwrap.dedent(
                    """
                    - Continue routine monitoring.
                    - Maintain prescribed medication.
                    - Encourage healthy lifestyle practices.
                    """
                )
            )

        elif predicted_risk == "Medium":
            st.warning(
                textwrap.dedent(
                    """
                    - Increase observation frequency.
                    - Schedule follow-up appointments.
                    - Monitor laboratory test results.
                    """
                )
            )

        elif predicted_risk == "High":
            st.error(
                textwrap.dedent(
                    """
                    - Recommend immediate physician review.
                    - Increase patient monitoring.
                    - Consider additional diagnostic tests.
                    """
                )
            )

        else:
            st.error(
                textwrap.dedent(
                    """
                    - Immediate intervention recommended.
                    - Admit for intensive monitoring.
                    - Escalate to senior medical staff.
                    """
                )
            )

    except Exception as ex:
        st.error(f"Prediction failed: {ex}")

# --------------------------------------------------
# Model Information
# --------------------------------------------------
st.divider()

st.subheader("📘 About This Model")

st.info(
    textwrap.dedent(
        """
        This machine learning model predicts a patient's healthcare
        risk category using demographic information, admission details,
        medical condition, medication history, and test results.

        The prediction is intended as an analytical aid and should not
        replace professional medical judgment.
        """
    )
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
show_footer()