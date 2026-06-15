import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About the Project")

st.markdown("""
# 🏥 Healthcare Risk Management Analytics System

This project is an interactive data analytics platform designed to analyze healthcare data,
identify potential risk factors, and provide meaningful insights through visual dashboards
and machine learning.

The application demonstrates how data-driven decision making can support hospitals,
healthcare administrators, and analysts in monitoring patient trends and operational metrics.
""")

st.divider()

# -------------------------------------------------
# Project Objectives
# -------------------------------------------------

st.header("🎯 Project Objectives")

st.markdown("""
- Analyze patient demographics and healthcare records.
- Monitor risk categories and identify high-risk patients.
- Explore admission trends and medical conditions.
- Visualize billing, medications, and insurance data.
- Use machine learning to predict patient risk levels.
- Support data-driven healthcare decision making.
""")

# -------------------------------------------------
# Features
# -------------------------------------------------

st.header("✨ Key Features")

st.markdown("""
- 📊 Executive Dashboard with KPIs
- 🏥 Patient Explorer with advanced filters
- 🚨 Risk Analysis Dashboard
- 🤖 AI-powered Risk Prediction
- 📈 Advanced Healthcare Analytics
- 📥 Download filtered data as CSV
- 🎛️ Interactive visualizations using Plotly
""")

# -------------------------------------------------
# Dataset
# -------------------------------------------------

st.header("📁 Dataset Information")

st.markdown("""
The project uses a synthetic healthcare dataset containing information such as:

- Patient demographics
- Medical conditions
- Admission and discharge dates
- Blood type
- Medications
- Test results
- Insurance providers
- Billing amounts
- Hospital details

The dataset is intended for educational and analytical purposes.
""")

# -------------------------------------------------
# Tech Stack
# -------------------------------------------------

st.header("🛠️ Technologies Used")

st.markdown("""
| Category | Technology |
|----------|------------|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| Machine Learning | Scikit-learn |
| Web Framework | Streamlit |
| Model Storage | Joblib |
""")

# -------------------------------------------------
# Risk Score
# -------------------------------------------------

st.header("🚨 Risk Assessment Logic")

st.markdown("""
The application estimates patient risk based on multiple factors such as:

- Senior citizen status
- Emergency admission
- Abnormal test results
- Length of hospital stay

These factors are combined into a risk score and categorized into:
- 🟢 Low
- 🟡 Medium
- 🟠 High
- 🔴 Critical
""")

# -------------------------------------------------
# Developer
# -------------------------------------------------

st.header("👨‍💻 Developer")

st.markdown("""
## Ayush Singh

**Role:** AI/ML Engineer & Data Analyst

### 🛠️ Technical Skills
- Python
- Machine Learning
- Data Analysis
- Data Visualization
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Matplotlib

### 🚀 About the Developer
Passionate about building intelligent, data-driven applications that solve real-world problems using Artificial Intelligence, Machine Learning, and Data Analytics. Experienced in developing interactive dashboards, predictive models, and end-to-end analytics solutions.

### 💡 Areas of Interest
- Artificial Intelligence
- Machine Learning
- Data Analytics
- Business Intelligence
- Predictive Modeling
- Healthcare Analytics
""")

st.divider()

st.success("🎉 Thank you for exploring the Healthcare Risk Management Analytics System!")