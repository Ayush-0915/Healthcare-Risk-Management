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
    page_title="Executive Dashboard",
    page_icon=str(logo_path),
    layout="wide"
)

load_css()

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
# Sidebar & Navigation
# --------------------------------------------------
render_sidebar()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Dashboard Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

risk_filter = st.sidebar.multiselect(
    "Risk Category",
    sorted(df["Risk Category"].dropna().unique()),
    default=sorted(df["Risk Category"].dropna().unique())
)

admission_filter = st.sidebar.multiselect(
    "Admission Type",
    sorted(df["Admission Type"].dropna().unique()),
    default=sorted(df["Admission Type"].dropna().unique())
)

filtered = df[
    df["Gender"].isin(gender_filter)
    & df["Risk Category"].isin(risk_filter)
    & df["Admission Type"].isin(admission_filter)
]

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📊 Executive Dashboard")
st.caption(
    "Monitor key healthcare metrics, admissions, billing, and patient risk."
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
total_patients = len(filtered)
high_risk = len(
    filtered[
        filtered["Risk Category"].isin(
            ["High", "Critical"]
        )
    ]
)

avg_age = filtered["Age"].mean()
avg_bill = filtered["Billing Amount"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Total Patients",
        f"{total_patients:,}",
        icon="👥",
        subtitle="Filtered Records",
        color="#2563EB"
    )

with c2:
    kpi_card(
        "High Risk",
        f"{high_risk:,}",
        icon="🚨",
        subtitle="High & Critical",
        color="#EF4444"
    )

with c3:
    kpi_card(
        "Average Age",
        f"{avg_age:.1f}",
        icon="🎂",
        subtitle="Years",
        color="#06B6D4"
    )

with c4:
    kpi_card(
        "Average Billing",
        f"${avg_bill:,.0f}",
        icon="💰",
        subtitle="USD",
        color="#10B981"
    )

st.divider()

# --------------------------------------------------
# Charts Row 1
# --------------------------------------------------
left, right = st.columns(2)

with left:

    fig = px.pie(
        filtered,
        names="Risk Category",
        hole=0.65,
        title="Risk Category Distribution"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    monthly = (
        filtered
        .groupby(
            filtered["Date of Admission"]
            .dt.to_period("M")
        )
        .size()
        .reset_index(name="Admissions")
    )

    monthly["Date of Admission"] = (
        monthly["Date of Admission"]
        .astype(str)
    )

    fig = px.line(
        monthly,
        x="Date of Admission",
        y="Admissions",
        markers=True,
        title="Monthly Admissions"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(
        fig,
        width="stretch"
    )

# --------------------------------------------------
# Charts Row 2
# --------------------------------------------------
left, right = st.columns(2)

with left:

    conditions = (
        filtered["Medical Condition"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    conditions.columns = [
        "Medical Condition",
        "Patients"
    ]

    fig = px.bar(
        conditions,
        x="Medical Condition",
        y="Patients",
        title="Top Medical Conditions",
        color="Patients",
        color_continuous_scale="Blues"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    fig = px.histogram(
        filtered,
        x="Age",
        color="Gender",
        nbins=20,
        title="Age Distribution"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(
        fig,
        width="stretch"
    )

# --------------------------------------------------
# Charts Row 3
# --------------------------------------------------
left, right = st.columns(2)

with left:

    billing = (
        filtered
        .groupby("Medical Condition")["Billing Amount"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        billing,
        x="Medical Condition",
        y="Billing Amount",
        title="Average Billing by Condition"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    fig = px.box(
        filtered,
        x="Risk Category",
        y="Length of Stay",
        title="Length of Stay by Risk"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(
        fig,
        width="stretch"
    )

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------
st.subheader("🧠 Executive Summary")

most_common = (
    filtered["Medical Condition"]
    .mode()[0]
)

st.success(
    f"""
- 👥 Total Patients: **{total_patients:,}**
- 🚨 High/Critical Patients: **{high_risk:,}**
- 🩺 Most Common Condition: **{most_common}**
- 💰 Average Billing: **${avg_bill:,.2f}**
- 🎂 Average Age: **{avg_age:.2f} years**
"""
)

# --------------------------------------------------
# Preview Data
# --------------------------------------------------
st.subheader("📋 Patient Records Preview")

preview_columns = [
    col for col in [
        "Name",
        "Age",
        "Gender",
        "Medical Condition",
        "Hospital",
        "Risk Category",
        "Billing Amount"
    ]
    if col in filtered.columns
]

st.dataframe(
    filtered[preview_columns].head(100),
    width="stretch",
    height=450
)

csv = filtered.to_csv(index=False)

st.download_button(
    "⬇️ Download Filtered Data",
    data=csv,
    file_name="executive_dashboard_data.csv",
    mime="text/csv"
)

show_footer()