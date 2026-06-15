import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------
st.set_page_config(
    page_title="Advanced Analytics",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------
@st.cache_data
def load_data():
    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "cleaned_healthcare_dataset.csv"
    )

    df = pd.read_csv(data_path)

    df["Date of Admission"] = pd.to_datetime(
        df["Date of Admission"]
    )

    return df


df = load_data()

# -------------------------------------------------------
# Title
# -------------------------------------------------------
st.title("📈 Advanced Healthcare Analytics")
st.caption(
    "Comprehensive insights into hospitals, billing, medications, insurance providers, and patient trends."
)

st.divider()

# -------------------------------------------------------
# KPI CARDS
# -------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🏥 Hospitals",
    df["Hospital"].nunique()
)

c2.metric(
    "👨‍⚕️ Doctors",
    df["Doctor"].nunique()
)

c3.metric(
    "💊 Medications",
    df["Medication"].nunique()
)

c4.metric(
    "🛡 Insurance Providers",
    df["Insurance Provider"].nunique()
)

st.divider()

# -------------------------------------------------------
# Monthly Admissions Trend
# -------------------------------------------------------
monthly = (
    df.groupby(
        df["Date of Admission"].dt.to_period("M")
    )
    .size()
    .reset_index(name="Admissions")
)

monthly["Date of Admission"] = monthly[
    "Date of Admission"
].astype(str)

fig = px.line(
    monthly,
    x="Date of Admission",
    y="Admissions",
    markers=True,
    title="📅 Monthly Admissions Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Top Hospitals
# -------------------------------------------------------
left, right = st.columns(2)

with left:

    hospitals = (
        df["Hospital"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    hospitals.columns = [
        "Hospital",
        "Patients"
    ]

    fig = px.bar(
        hospitals,
        x="Hospital",
        y="Patients",
        title="🏥 Top Hospitals"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    insurance = (
        df["Insurance Provider"]
        .value_counts()
        .reset_index()
    )

    insurance.columns = [
        "Insurance",
        "Patients"
    ]

    fig = px.pie(
        insurance,
        names="Insurance",
        values="Patients",
        hole=0.5,
        title="🛡 Insurance Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Medication Analysis
# -------------------------------------------------------
left, right = st.columns(2)

with left:

    meds = (
        df["Medication"]
        .value_counts()
        .reset_index()
    )

    meds.columns = [
        "Medication",
        "Count"
    ]

    fig = px.bar(
        meds,
        x="Medication",
        y="Count",
        title="💊 Medication Usage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    tests = (
        df["Test Results"]
        .value_counts()
        .reset_index()
    )

    tests.columns = [
        "Result",
        "Count"
    ]

    fig = px.pie(
        tests,
        names="Result",
        values="Count",
        title="🧪 Test Result Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Billing by Condition
# -------------------------------------------------------
billing = (
    df.groupby(
        "Medical Condition"
    )["Billing Amount"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    billing,
    x="Medical Condition",
    y="Billing Amount",
    title="💰 Average Billing by Medical Condition"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Age Distribution by Gender
# -------------------------------------------------------
fig = px.histogram(
    df,
    x="Age",
    color="Gender",
    nbins=30,
    title="👥 Age Distribution by Gender"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Length of Stay Analysis
# -------------------------------------------------------
fig = px.box(
    df,
    x="Risk Category",
    y="Length of Stay",
    title="🛏 Length of Stay by Risk Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Executive Summary
# -------------------------------------------------------
st.divider()

st.subheader("📋 Executive Summary")

top_condition = (
    df["Medical Condition"]
    .value_counts()
    .idxmax()
)

top_hospital = (
    df["Hospital"]
    .value_counts()
    .idxmax()
)

top_medication = (
    df["Medication"]
    .value_counts()
    .idxmax()
)

st.success(f"""
### Key Findings

- 👥 Total Patients: **{len(df):,}**
- 🏥 Total Hospitals: **{df['Hospital'].nunique()}**
- 👨‍⚕️ Total Doctors: **{df['Doctor'].nunique()}**
- 🩺 Most Common Condition: **{top_condition}**
- 🏥 Hospital with Highest Admissions: **{top_hospital}**
- 💊 Most Prescribed Medication: **{top_medication}**
- 💰 Average Billing Amount: **${df['Billing Amount'].mean():,.2f}**
- 🛏 Average Length of Stay: **{df['Length of Stay'].mean():.2f} days**
- 🎂 Average Patient Age: **{df['Age'].mean():.2f} years**
""")