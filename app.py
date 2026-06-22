import streamlit as st
import pandas as pd
import textwrap
from pathlib import Path

from components.theme import load_css
from components.hero import hero
from components.cards import kpi_card
from components.footer import show_footer
from components.sidebar import render_sidebar

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

logo_path = BASE_DIR / "assets" / "logo.png"

st.set_page_config(
    page_title="Healthcare Risk Management Analytics",
    page_icon=str(logo_path),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Load Theme
# ---------------------------------------------------
load_css()

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------
@st.cache_data
def load_data():
    data_path = (
        BASE_DIR
        / "data"
        / "cleaned_healthcare_dataset.csv"
    )

    return pd.read_csv(data_path)

df = load_data()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
render_sidebar()

# ---------------------------------------------------
# Hero Section
# ---------------------------------------------------
hero()

# ---------------------------------------------------
# Live KPI Metrics
# ---------------------------------------------------
total_patients = len(df)

avg_age = round(df["Age"].mean(), 1)

avg_billing = round(
    df["Billing Amount"].mean(),
    0
)

avg_stay = round(
    df["Length of Stay"].mean(),
    1
)

# ---------------------------------------------------
# Dashboard Overview
# ---------------------------------------------------
st.markdown("## 📊 Platform Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Total Patients",
        f"{total_patients:,}",
        "👥",
        "Healthcare Records",
        "#2563EB"
    )

with c2:
    kpi_card(
        "Average Age",
        f"{avg_age}",
        "🎂",
        "Patient Demographics",
        "#06B6D4"
    )

with c3:
    kpi_card(
        "Average Billing",
        f"${avg_billing:,.0f}",
        "💰",
        "Per Patient",
        "#10B981"
    )

with c4:
    kpi_card(
        "Average Stay",
        f"{avg_stay} Days",
        "🛏️",
        "Hospital Duration",
        "#F59E0B"
    )

st.markdown("---")

# ---------------------------------------------------
# Welcome Section
# ---------------------------------------------------
left, right = st.columns([1.4, 1])

with left:

    st.markdown(
        textwrap.dedent(
            """
            ## 🚀 Welcome

            The Healthcare Risk Management Analytics System
            helps healthcare professionals leverage
            Data Analytics and Machine Learning
            for smarter decision-making.

            ### Features

            - 📊 Interactive Dashboards
            - 🚨 Risk Analysis
            - 🤖 AI Predictions
            - 📈 Advanced Analytics
            - 🏥 Patient Exploration
            - 📋 Executive Insights
            """
        )
    )

with right:

    st.info(
        textwrap.dedent(
            """
            ### 📌 Quick Start

            1️⃣ Open Executive Dashboard

            2️⃣ Explore Patient Explorer

            3️⃣ Analyze Risk Trends

            4️⃣ Predict Patient Risk

            5️⃣ Review Advanced Analytics
            """
        )
    )

st.markdown("---")

# ---------------------------------------------------
# Feature Cards
# ---------------------------------------------------
st.markdown("## ✨ Platform Modules")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(
        textwrap.dedent(
            """
            <div class="glass-card">
                <h3>📊 Executive Dashboard</h3>
                <p>
                    Monitor healthcare KPIs,
                    admissions, billing trends,
                    and patient demographics.
                </p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

with f2:
    st.markdown(
        textwrap.dedent(
            """
            <div class="glass-card">
                <h3>🚨 Risk Analysis</h3>
                <p>
                    Identify high-risk patients,
                    analyze medical conditions,
                    and monitor risk distribution.
                </p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

with f3:
    st.markdown(
        textwrap.dedent(
            """
            <div class="glass-card">
                <h3>🤖 AI Predictions</h3>
                <p>
                    Use Machine Learning to predict
                    healthcare risk categories
                    from patient information.
                </p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# Statistics Preview
# ---------------------------------------------------
st.markdown("## 📈 Dataset Snapshot")

preview_cols = [
    "Age",
    "Gender",
    "Medical Condition",
    "Hospital",
    "Risk Category"
]

available_cols = [
    c for c in preview_cols
    if c in df.columns
]

st.dataframe(
    df[available_cols].head(20),
    use_container_width=True
)

st.success(
    "🎯 Use the sidebar navigation to explore dashboards, analytics, and AI-powered healthcare insights."
)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
show_footer()