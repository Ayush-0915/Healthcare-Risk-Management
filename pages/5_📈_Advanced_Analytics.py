import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from components.theme import load_css
from components.cards import kpi_card
from components.footer import show_footer
from components.plotly_theme import apply_plotly_theme
from components.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
logo_path = BASE_DIR / "assets" / "logo.png"

st.set_page_config(
    page_title="Advanced Analytics",
    page_icon=str(logo_path),
    layout="wide"
)

load_css()

# --------------------------------------------------
# Sidebar & Navigation
# --------------------------------------------------
render_sidebar()

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        BASE_DIR / "data" / "cleaned_healthcare_dataset.csv"
    )

    df["Date of Admission"] = pd.to_datetime(
        df["Date of Admission"],
        errors="coerce"
    )

    return df

df = load_data()

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📈 Advanced Analytics")
st.caption(
    "Executive-level insights into admissions, hospitals, medications, insurance, and billing."
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Hospitals",
        str(df["Hospital"].nunique()),
        icon="🏥",
        subtitle="Unique Hospitals",
        color="#2563EB"
    )

with c2:
    kpi_card(
        "Doctors",
        str(df["Doctor"].nunique()),
        icon="👨‍⚕️",
        subtitle="Unique Doctors",
        color="#06B6D4"
    )

with c3:
    kpi_card(
        "Insurance Providers",
        str(df["Insurance Provider"].nunique()),
        icon="🛡️",
        subtitle="Providers",
        color="#10B981"
    )

with c4:
    kpi_card(
        "Medications",
        str(df["Medication"].nunique()),
        icon="💊",
        subtitle="Available",
        color="#F59E0B"
    )

st.divider()

# --------------------------------------------------
# Monthly Admissions
# --------------------------------------------------
monthly = (
    df.groupby(df["Date of Admission"].dt.to_period("M"))
    .size()
    .reset_index(name="Admissions")
)

monthly["Date of Admission"] = monthly["Date of Admission"].astype(str)

fig = px.line(
    monthly,
    x="Date of Admission",
    y="Admissions",
    markers=True,
    title="📅 Monthly Admissions"
)

fig = apply_plotly_theme(fig)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Row 1
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    hospitals = (
        df["Hospital"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    hospitals.columns = ["Hospital", "Patients"]

    fig = px.bar(
        hospitals,
        x="Hospital",
        y="Patients",
        title="🏥 Top Hospitals"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    insurance = (
        df["Insurance Provider"]
        .value_counts()
        .reset_index()
    )

    insurance.columns = ["Provider", "Patients"]

    fig = px.pie(
        insurance,
        names="Provider",
        values="Patients",
        hole=0.65,
        title="🛡️ Insurance Distribution"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Row 2
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    meds = (
        df["Medication"]
        .value_counts()
        .reset_index()
    )

    meds.columns = ["Medication", "Count"]

    fig = px.bar(
        meds,
        x="Medication",
        y="Count",
        title="💊 Medication Usage"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    billing = (
        df.groupby("Medical Condition")["Billing Amount"]
        .mean()
        .reset_index()
        .sort_values(
            by="Billing Amount",
            ascending=False
        )
    )

    fig = px.bar(
        billing,
        x="Medical Condition",
        y="Billing Amount",
        title="💰 Average Billing by Condition"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Length of Stay
# --------------------------------------------------
fig = px.box(
    df,
    x="Risk Category",
    y="Length of Stay",
    title="🛏️ Length of Stay by Risk Category"
)

fig = apply_plotly_theme(fig)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Executive Insights
# --------------------------------------------------
st.subheader("🧠 Executive Insights")

top_condition = df["Medical Condition"].mode()[0]
top_hospital = df["Hospital"].mode()[0]
top_medication = df["Medication"].mode()[0]

st.success(f"""
- 👥 Total Records: **{len(df):,}**
- 🩺 Most Common Condition: **{top_condition}**
- 🏥 Most Active Hospital: **{top_hospital}**
- 💊 Most Used Medication: **{top_medication}**
- 💰 Average Billing: **${df['Billing Amount'].mean():,.2f}**
- 🛏️ Average Length of Stay: **{df['Length of Stay'].mean():.2f} Days**
""")

# --------------------------------------------------
# Download
# --------------------------------------------------
csv = df.to_csv(index=False)

st.download_button(
    "⬇️ Download Dataset",
    data=csv,
    file_name="healthcare_dataset.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
show_footer()