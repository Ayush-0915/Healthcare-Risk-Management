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
    page_title="Risk Analysis",
    page_icon=str(logo_path),
    layout="wide"
)

load_css()

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        BASE_DIR / "data" / "cleaned_healthcare_dataset.csv"
    )


df = load_data()

# --------------------------------------------------
# Sidebar & Navigation
# --------------------------------------------------
render_sidebar()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🎛️ Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Category",
    sorted(df["Risk Category"].dropna().unique()),
    default=sorted(df["Risk Category"].dropna().unique())
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

condition_filter = st.sidebar.multiselect(
    "Medical Condition",
    sorted(df["Medical Condition"].dropna().unique()),
    default=sorted(df["Medical Condition"].dropna().unique())
)

filtered = df[
    df["Risk Category"].isin(risk_filter)
    & df["Gender"].isin(gender_filter)
    & df["Medical Condition"].isin(condition_filter)
]

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
high_risk = filtered[
    filtered["Risk Category"].isin(["High", "Critical"])
]

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Total Patients",
        f"{len(filtered):,}",
        icon="👥",
        subtitle="Filtered Records",
        color="#2563EB"
    )

with c2:
    kpi_card(
        "High Risk",
        f"{len(high_risk):,}",
        icon="🚨",
        subtitle="High & Critical",
        color="#EF4444"
    )

with c3:
    kpi_card(
        "Avg Billing",
        f"${filtered['Billing Amount'].mean():,.0f}",
        icon="💰",
        subtitle="USD",
        color="#10B981"
    )

with c4:
    kpi_card(
        "Avg Stay",
        f"{filtered['Length of Stay'].mean():.1f} Days",
        icon="🛏️",
        subtitle="Hospital Stay",
        color="#F59E0B"
    )

st.divider()

# --------------------------------------------------
# Charts Row 1
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        filtered,
        names="Risk Category",
        hole=0.65,
        title="Risk Category Distribution"
    )
    fig = apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    admission = (
        filtered.groupby(
            ["Admission Type", "Risk Category"]
        )
        .size()
        .reset_index(name="Patients")
    )

    fig = px.bar(
        admission,
        x="Admission Type",
        y="Patients",
        color="Risk Category",
        barmode="group",
        title="Admission Type vs Risk"
    )

    fig = apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Charts Row 2
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    top_conditions = (
        high_risk["Medical Condition"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_conditions.columns = [
        "Medical Condition",
        "Patients"
    ]

    fig = px.bar(
        top_conditions,
        x="Medical Condition",
        y="Patients",
        title="Top High-Risk Medical Conditions"
    )

    fig = apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    billing = (
        filtered.groupby("Risk Category")[
            "Billing Amount"
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        billing,
        x="Risk Category",
        y="Billing Amount",
        title="Average Billing by Risk"
    )

    fig = apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Charts Row 3
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    fig = px.box(
        filtered,
        x="Risk Category",
        y="Length of Stay",
        title="Length of Stay by Risk"
    )

    fig = apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    gender_risk = (
        filtered.groupby(
            ["Gender", "Risk Category"]
        )
        .size()
        .reset_index(name="Patients")
    )

    fig = px.bar(
        gender_risk,
        x="Gender",
        y="Patients",
        color="Risk Category",
        barmode="group",
        title="Gender vs Risk Category"
    )

    fig = apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------
st.subheader("🧠 Executive Insights")

st.success(f"""
- 👥 Total Patients: **{len(filtered):,}**
- 🚨 High/Critical Patients: **{len(high_risk):,}**
- 💰 Average Billing: **${filtered['Billing Amount'].mean():,.2f}**
- 🛏️ Average Stay: **{filtered['Length of Stay'].mean():.2f} Days**
- 🩺 Most Common Condition: **{filtered['Medical Condition'].mode()[0]}**
""")

# --------------------------------------------------
# High Risk Patient Table
# --------------------------------------------------
st.subheader("📋 High-Risk Patients")

display_columns = [
    col for col in [
        "Name",
        "Age",
        "Gender",
        "Medical Condition",
        "Hospital",
        "Doctor",
        "Risk Category",
        "Billing Amount",
        "Length of Stay"
    ]
    if col in high_risk.columns
]

st.dataframe(
    high_risk[display_columns],
    use_container_width=True,
    height=450
)

csv = high_risk.to_csv(index=False)

st.download_button(
    "⬇ Download High-Risk Patients",
    data=csv,
    file_name="high_risk_patients.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
show_footer()