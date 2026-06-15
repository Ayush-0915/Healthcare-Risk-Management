import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Executive Dashboard", layout="wide")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_healthcare_dataset.csv")
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

admission = st.sidebar.multiselect(
    "Admission Type",
    sorted(df["Admission Type"].unique()),
    default=sorted(df["Admission Type"].unique())
)

risk = st.sidebar.multiselect(
    "Risk Category",
    sorted(df["Risk Category"].unique()),
    default=sorted(df["Risk Category"].unique())
)

filtered = df[
    df["Gender"].isin(gender)
    & df["Admission Type"].isin(admission)
    & df["Risk Category"].isin(risk)
]

# -----------------------------
# Title
# -----------------------------
st.title("🏥 Executive Dashboard")
st.caption("Real-time overview of healthcare risk metrics")

# -----------------------------
# KPI Cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Total Patients", f"{len(filtered):,}")
c2.metric("🎂 Avg Age", f"{filtered['Age'].mean():.1f}")
c3.metric("💰 Avg Billing", f"${filtered['Billing Amount'].mean():,.0f}")
c4.metric("🛏 Avg Stay", f"{filtered['Length of Stay'].mean():.1f} Days")

st.divider()

# -----------------------------
# Charts Row 1
# -----------------------------
left, right = st.columns(2)

with left:
    fig = px.histogram(
        filtered,
        x="Age",
        nbins=25,
        title="Age Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.pie(
        filtered,
        names="Risk Category",
        title="Risk Category Distribution",
        hole=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Charts Row 2
# -----------------------------
left, right = st.columns(2)

with left:
    cond = (
        filtered["Medical Condition"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    cond.columns = ["Medical Condition", "Count"]

    fig = px.bar(
        cond,
        x="Medical Condition",
        y="Count",
        title="Top Medical Conditions"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.pie(
        filtered,
        names="Admission Type",
        title="Admission Type Breakdown"
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Monthly Trend
# -----------------------------
monthly = (
    filtered
    .groupby(filtered["Date of Admission"].dt.to_period("M"))
    .size()
    .reset_index(name="Admissions")
)

monthly["Date of Admission"] = (
    monthly["Date of Admission"].astype(str)
)

fig = px.line(
    monthly,
    x="Date of Admission",
    y="Admissions",
    markers=True,
    title="Monthly Admissions Trend"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Data Preview
# -----------------------------
st.subheader("📋 Data Preview")
st.dataframe(filtered.head(100), use_container_width=True)

csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_patients.csv",
    "text/csv"
)