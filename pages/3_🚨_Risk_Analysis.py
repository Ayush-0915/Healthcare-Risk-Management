import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Risk Analysis",
    page_icon="🚨",
    layout="wide"
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "cleaned_healthcare_dataset.csv"
    )
    return pd.read_csv(data_path)

df = load_data()

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🚨 Healthcare Risk Analysis Dashboard")
st.markdown("Analyze patient risk levels and identify high-risk patterns.")

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("🔍 Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Category",
    sorted(df["Risk Category"].unique()),
    default=sorted(df["Risk Category"].unique())
)

condition_filter = st.sidebar.multiselect(
    "Medical Condition",
    sorted(df["Medical Condition"].unique()),
    default=sorted(df["Medical Condition"].unique())
)

filtered = df[
    df["Risk Category"].isin(risk_filter)
    & df["Medical Condition"].isin(condition_filter)
]

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
high_risk = filtered[
    filtered["Risk Category"].isin(["High", "Critical"])
]

c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Total Patients", f"{len(filtered):,}")
c2.metric("🚨 High Risk", f"{len(high_risk):,}")
c3.metric(
    "🛏 Avg Stay",
    f"{filtered['Length of Stay'].mean():.1f} Days"
)
c4.metric(
    "💰 Avg Billing",
    f"${filtered['Billing Amount'].mean():,.0f}"
)

st.divider()

# -------------------------------------------------
# Risk Distribution
# -------------------------------------------------
left, right = st.columns(2)

with left:
    fig = px.pie(
        filtered,
        names="Risk Category",
        hole=0.55,
        title="Risk Category Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    risk_counts = (
        filtered["Risk Category"]
        .value_counts()
        .reset_index()
    )
    risk_counts.columns = ["Risk Category", "Count"]

    fig = px.bar(
        risk_counts,
        x="Risk Category",
        y="Count",
        title="Patients by Risk Category",
        text="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Top Medical Conditions
# -------------------------------------------------
condition_counts = (
    filtered["Medical Condition"]
    .value_counts()
    .head(10)
    .reset_index()
)

condition_counts.columns = [
    "Medical Condition",
    "Patients"
]

fig = px.bar(
    condition_counts,
    x="Medical Condition",
    y="Patients",
    title="Top Medical Conditions"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Billing by Risk
# -------------------------------------------------
billing = (
    filtered.groupby("Risk Category")["Billing Amount"]
    .mean()
    .reset_index()
)

fig = px.bar(
    billing,
    x="Risk Category",
    y="Billing Amount",
    title="Average Billing by Risk Category",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Length of Stay by Risk
# -------------------------------------------------
stay = (
    filtered.groupby("Risk Category")["Length of Stay"]
    .mean()
    .reset_index()
)

fig = px.bar(
    stay,
    x="Risk Category",
    y="Length of Stay",
    title="Average Length of Stay by Risk Category",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# High-Risk Table
# -------------------------------------------------
st.subheader("🚨 High-Risk Patient Records")

display_cols = [
    "Name",
    "Age",
    "Gender",
    "Medical Condition",
    "Hospital",
    "Admission Type",
    "Risk Category",
    "Billing Amount",
    "Length of Stay",
]

st.dataframe(
    high_risk[display_cols],
    use_container_width=True,
    height=450
)

# -------------------------------------------------
# Executive Insights
# -------------------------------------------------
st.divider()
st.subheader("📌 Executive Insights")

most_common = filtered["Medical Condition"].mode()[0]

st.success(
    f"""
- 👥 Total filtered patients: **{len(filtered):,}**
- 🚨 High/Critical risk patients: **{len(high_risk):,}**
- 🩺 Most common medical condition: **{most_common}**
- 💰 Average billing: **${filtered['Billing Amount'].mean():,.2f}**
- 🛏 Average length of stay: **{filtered['Length of Stay'].mean():.2f} days**
"""
)

# -------------------------------------------------
# Download
# -------------------------------------------------
csv = high_risk.to_csv(index=False)

st.download_button(
    "⬇️ Download High-Risk Patients",
    data=csv,
    file_name="high_risk_patients.csv",
    mime="text/csv"
)