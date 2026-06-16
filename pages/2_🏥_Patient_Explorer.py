import streamlit as st
import pandas as pd
from pathlib import Path

from components.theme import load_css
from components.cards import kpi_card
from components.footer import show_footer
from components.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
logo_path = BASE_DIR / "assets" / "logo.png"

st.set_page_config(
    page_title="Patient Explorer",
    page_icon=str(logo_path),
    layout="wide"
)

load_css()

# --------------------------------------------------
# Load Dataset
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
st.sidebar.header("🔍 Filters")

search_text = st.sidebar.text_input(
    "Search Patient Name"
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

age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered = df.copy()

filtered = filtered[
    filtered["Gender"].isin(gender_filter)
]

filtered = filtered[
    filtered["Medical Condition"].isin(condition_filter)
]

filtered = filtered[
    filtered["Risk Category"].isin(risk_filter)
]

filtered = filtered[
    filtered["Admission Type"].isin(admission_filter)
]

filtered = filtered[
    (filtered["Age"] >= age_range[0])
    &
    (filtered["Age"] <= age_range[1])
]

if (
    search_text
    and "Name" in filtered.columns
):
    filtered = filtered[
        filtered["Name"].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# --------------------------------------------------
# Summary
# --------------------------------------------------
st.markdown("## 📊 Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Patients",
        f"{len(filtered):,}",
        icon="👥",
        subtitle="Filtered Records",
        color="#2563EB"
    )

with c2:
    kpi_card(
        "Average Age",
        f"{filtered['Age'].mean():.1f}",
        icon="🎂",
        subtitle="Years",
        color="#06B6D4"
    )

with c3:
    kpi_card(
        "Average Billing",
        f"${filtered['Billing Amount'].mean():,.0f}",
        icon="💰",
        subtitle="USD",
        color="#10B981"
    )

with c4:
    kpi_card(
        "Average Stay",
        f"{filtered['Length of Stay'].mean():.1f}",
        icon="🛏️",
        subtitle="Days",
        color="#F59E0B"
    )

st.divider()

# --------------------------------------------------
# Sort Options
# --------------------------------------------------
sort_column = st.selectbox(
    "Sort By",
    [
        "Age",
        "Billing Amount",
        "Length of Stay"
    ]
)

ascending = st.checkbox(
    "Ascending",
    value=True
)

filtered = filtered.sort_values(
    by=sort_column,
    ascending=ascending
)

# --------------------------------------------------
# Data Table
# --------------------------------------------------
st.subheader("📋 Patient Records")

display_columns = [
    col for col in [
        "Name",
        "Age",
        "Gender",
        "Blood Type",
        "Medical Condition",
        "Admission Type",
        "Hospital",
        "Doctor",
        "Medication",
        "Test Results",
        "Risk Category",
        "Billing Amount",
        "Length of Stay"
    ]
    if col in filtered.columns
]

st.dataframe(
    filtered[display_columns],
    width="stretch",
    height=550
)

# --------------------------------------------------
# Download
# --------------------------------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    data=csv,
    file_name="patient_explorer.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Quick Insights
# --------------------------------------------------
st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🏥 Top Medical Conditions")

    st.dataframe(
        filtered["Medical Condition"]
        .value_counts()
        .head(10)
        .rename_axis("Condition")
        .reset_index(name="Patients"),
        width="stretch"
    )

with right:

    st.subheader("🏥 Top Hospitals")

    st.dataframe(
        filtered["Hospital"]
        .value_counts()
        .head(10)
        .rename_axis("Hospital")
        .reset_index(name="Patients"),
        width="stretch"
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
show_footer()