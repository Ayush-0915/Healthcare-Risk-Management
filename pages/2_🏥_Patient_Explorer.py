import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Patient Explorer",
    page_icon="🏥",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "cleaned_healthcare_dataset.csv"
    )
    return pd.read_csv(data_path)

df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("🏥 Patient Explorer")
st.markdown("Search, filter, and explore patient records interactively.")

# -----------------------------
# Search Bar
# -----------------------------
search_name = st.text_input(
    "🔍 Search by Patient Name",
    placeholder="Enter patient name..."
)

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("🎛️ Filters")

gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

condition = st.sidebar.multiselect(
    "Medical Condition",
    sorted(df["Medical Condition"].dropna().unique()),
    default=sorted(df["Medical Condition"].dropna().unique())
)

admission = st.sidebar.multiselect(
    "Admission Type",
    sorted(df["Admission Type"].dropna().unique()),
    default=sorted(df["Admission Type"].dropna().unique())
)

risk = st.sidebar.multiselect(
    "Risk Category",
    sorted(df["Risk Category"].dropna().unique()),
    default=sorted(df["Risk Category"].dropna().unique())
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered = df.copy()

filtered = filtered[
    filtered["Gender"].isin(gender)
]

filtered = filtered[
    filtered["Medical Condition"].isin(condition)
]

filtered = filtered[
    filtered["Admission Type"].isin(admission)
]

filtered = filtered[
    filtered["Risk Category"].isin(risk)
]

filtered = filtered[
    (filtered["Age"] >= age_range[0]) &
    (filtered["Age"] <= age_range[1])
]

if search_name:
    filtered = filtered[
        filtered["Name"].str.contains(
            search_name,
            case=False,
            na=False
        )
    ]

# -----------------------------
# Summary Cards
# -----------------------------
c1, c2, c3 = st.columns(3)

c1.metric("👥 Patients Found", len(filtered))
c2.metric("🎂 Average Age", f"{filtered['Age'].mean():.1f}")
c3.metric("💰 Avg Billing", f"${filtered['Billing Amount'].mean():,.0f}")

st.divider()

# -----------------------------
# Sort Options
# -----------------------------
sort_column = st.selectbox(
    "Sort By",
    [
        "Age",
        "Billing Amount",
        "Length of Stay",
        "Name"
    ]
)

ascending = st.checkbox("Sort Ascending", value=True)

filtered = filtered.sort_values(
    by=sort_column,
    ascending=ascending
)

# -----------------------------
# Display Table
# -----------------------------
st.subheader("📋 Patient Records")

st.dataframe(
    filtered,
    use_container_width=True,
    height=600
)

# -----------------------------
# Download Button
# -----------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="patient_records.csv",
    mime="text/csv"
)

# -----------------------------
# Quick Statistics
# -----------------------------
st.divider()
st.subheader("📊 Quick Insights")

left, right = st.columns(2)

with left:
    st.write("**Top 5 Medical Conditions**")
    st.dataframe(
        filtered["Medical Condition"]
        .value_counts()
        .head(5)
        .rename_axis("Condition")
        .reset_index(name="Count"),
        use_container_width=True
    )

with right:
    st.write("**Top 5 Hospitals by Patient Count**")
    st.dataframe(
        filtered["Hospital"]
        .value_counts()
        .head(5)
        .rename_axis("Hospital")
        .reset_index(name="Patients"),
        use_container_width=True
    )