import streamlit as st
import textwrap
from pathlib import Path

from components.theme import load_css
from components.footer import show_footer
from components.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
logo_path = BASE_DIR / "assets" / "logo.png"

st.set_page_config(
    page_title="About",
    page_icon=str(logo_path),
    layout="wide"
)

load_css()

# --------------------------------------------------
# Sidebar & Navigation
# --------------------------------------------------
render_sidebar()

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("ℹ️ About This Project")
st.caption("Healthcare Risk Management Analytics System")

st.markdown("---")

# --------------------------------------------------
# Developer Section
# --------------------------------------------------
col1, col2 = st.columns([1, 3])

with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=180)

with col2:
    st.markdown(
        textwrap.dedent(
            """
            # 👨‍💻 Ayush Singh

            ### AI/ML Engineer & Data Analyst

            Passionate about building intelligent data-driven applications
            using Artificial Intelligence, Machine Learning, Python,
            and Data Analytics.

            Special interests:
            - 🤖 Machine Learning
            - 📊 Data Analytics
            - 🐍 Python Development
            - 📈 Business Intelligence
            - 🏥 Healthcare Analytics
            - ☁️ Streamlit Deployment
            """
        )
    )

st.markdown("---")

# --------------------------------------------------
# Project Overview
# --------------------------------------------------
st.header("🏥 Project Overview")

st.markdown(
    textwrap.dedent(
        """
        The **Healthcare Risk Management Analytics System** is an end-to-end
        data analytics and machine learning application designed to analyze
        healthcare records and predict patient risk levels.

        ### Key Objectives

        - 📊 Analyze healthcare datasets
        - 🚨 Identify high-risk patients
        - 🤖 Predict risk using Machine Learning
        - 📈 Generate executive dashboards
        - 🏥 Support healthcare decision-making
        """
    )
)

st.markdown("---")

# --------------------------------------------------
# Features
# --------------------------------------------------
st.header("✨ Features")

col1, col2 = st.columns(2)

with col1:
    st.success(
        textwrap.dedent(
            """
            - 📊 Executive Dashboard
            - 🏥 Patient Explorer
            - 🚨 Risk Analysis
            - 🤖 AI Risk Prediction
            """
        )
    )

with col2:
    st.success(
        textwrap.dedent(
            """
            - 📈 Advanced Analytics
            - 📥 CSV Export
            - 🎨 Interactive Visualizations
            - 💻 Responsive Streamlit UI
            """
        )
    )

st.markdown("---")

# --------------------------------------------------
# Tech Stack
# --------------------------------------------------
st.header("🛠️ Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.info(
        textwrap.dedent(
            """
            ### Programming
            - Python
            - Pandas
            - NumPy
            - Joblib
            """
        )
    )

with tech2:
    st.info(
        textwrap.dedent(
            """
            ### Visualization
            - Plotly
            - Streamlit
            - CSS
            - HTML
            """
        )
    )

with tech3:
    st.info(
        textwrap.dedent(
            """
            ### Machine Learning
            - Scikit-learn
            - Label Encoding
            - Classification Models
            - Risk Prediction
            """
        )
    )

st.markdown("---")

# --------------------------------------------------
# Dataset Summary
# --------------------------------------------------
st.header("📂 Dataset Highlights")

st.markdown(
    textwrap.dedent(
        """
        The application analyzes healthcare records containing:

        - 👤 Age
        - 🚻 Gender
        - 🩸 Blood Type
        - 🏥 Hospital
        - 👨‍⚕️ Doctor
        - 🩺 Medical Condition
        - 💊 Medication
        - 📋 Test Results
        - 💰 Billing Amount
        - 🛏️ Length of Stay
        - 🚨 Risk Category
        """
    )
)

st.markdown("---")

# --------------------------------------------------
# Live Application
# --------------------------------------------------
st.header("🌐 Live Demo")

st.success(
    "🚀 https://healthcare-risk-management.streamlit.app/"
)

st.markdown("---")

# --------------------------------------------------
# Contact
# --------------------------------------------------
st.header("📬 Contact")

st.markdown(
    textwrap.dedent(
        """
        ### 👨‍💻 Ayush Singh

        - 💼 Role: **AI/ML Engineer & Data Analyst**
        - 🌍 Portfolio Project: **Healthcare Risk Management Analytics System**

        You can add your GitHub and LinkedIn profile links here before publishing.
        """
    )
)

st.markdown("---")

# --------------------------------------------------
# Footer
# --------------------------------------------------
show_footer()