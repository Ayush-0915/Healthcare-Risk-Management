import streamlit as st
import textwrap
from pathlib import Path

# Base Directory relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
logo_path = BASE_DIR / "assets" / "logo.png"


def render_sidebar():
    """
    Renders the custom, unified sidebar with branding, glassmorphic page link navigation, and developer info.
    """
    # 1. Sidebar Logo & Branding
    if logo_path.exists():
        st.sidebar.image(
            str(logo_path),
            width="stretch"
        )

    st.sidebar.markdown(
        textwrap.dedent(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="margin: 0; color: white; font-size: 22px; font-weight: 800; letter-spacing: -0.5px;">🏥 Healthcare Analytics</h2>
                <p style="margin: 5px 0 0 0; color: #38bdf8; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Risk Analytics Platform
                </p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    # 2. Sidebar Navigation using st.page_link
    st.sidebar.markdown(
        "<p style='color: #94a3b8; font-weight: 700; font-size: 11px; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.5px;'>Navigation</p>",
        unsafe_allow_html=True
    )

    st.sidebar.page_link("app.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/1_📊_Executive_Dashboard.py", label="Executive Dashboard", icon="📊")
    st.sidebar.page_link("pages/2_🏥_Patient_Explorer.py", label="Patient Explorer", icon="🏥")
    st.sidebar.page_link("pages/3_🚨_Risk_Analysis.py", label="Risk Analysis", icon="🚨")
    st.sidebar.page_link("pages/4_🤖_ML_Predictions.py", label="ML Predictions", icon="🤖")
    st.sidebar.page_link("pages/5_📈_Advanced_Analytics.py", label="Advanced Analytics", icon="📈")
    st.sidebar.page_link("pages/6_ℹ️_About.py", label="About", icon="ℹ️")

    st.sidebar.markdown("---")

    # 3. Developer Card Info
    st.sidebar.markdown(
        textwrap.dedent(
            """
            <div style="background: rgba(255, 255, 255, 0.03); padding: 16px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);">
                <p style="margin: 0; color: #94a3b8; font-size: 10px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Developer</p>
                <p style="margin: 6px 0 0 0; color: #ffffff; font-weight: 700; font-size: 14px;">Ayush Singh</p>
                <p style="margin: 2px 0 0 0; color: #38bdf8; font-size: 12px; font-weight: 500;">AI/ML Engineer & Analyst</p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )
