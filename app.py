import streamlit as st

st.set_page_config(
    page_title="Healthcare Risk Management Analytics",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Risk Management Analytics Platform")

st.markdown("""
Welcome to the **Healthcare Risk Management Analytics Platform**.

This application provides interactive dashboards and analytics for:
- 📊 Executive Dashboard
- 🏥 Patient Explorer
- 🚨 Risk Analysis
- 🤖 Machine Learning Predictions
- 📈 Advanced Analytics
- ℹ️ About the Project

Use the **sidebar on the left** to navigate between pages.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Dataset", "55,500 Records")

with col2:
    st.metric("Analysis", "Interactive")

with col3:
    st.metric("ML Ready", "✅")

st.info(
    "Built with Streamlit, Pandas, Plotly, and Scikit-learn for healthcare analytics."
)