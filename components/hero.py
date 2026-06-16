import streamlit as st
import base64
import textwrap
from pathlib import Path

# --------------------------------------------------
# Base Directory
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


def get_base64_image(image_path):
    """
    Convert an image file to a base64 string.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def hero():
    """
    Display the hero banner on the homepage.
    """

    hero_image = BASE_DIR / "assets" / "hero.jpg"

    if not hero_image.exists():
        st.warning("⚠️ Hero image not found in assets/hero.jpg")
        return

    encoded_image = get_base64_image(hero_image)

    # We use textwrap.dedent and inline styling for dynamic background-image
    # all other static classes are defined in style.css
    html_content = textwrap.dedent(
        f"""
        <div class="hero-container" style="background-image: linear-gradient(rgba(5, 15, 35, 0.75), rgba(5, 15, 35, 0.75)), url('data:image/jpeg;base64,{encoded_image}');">
            <div class="hero-content">
                <div class="hero-title">🏥 Healthcare Risk Management</div>
                <div class="hero-subtitle">AI-Powered Analytics Platform</div>
                <div class="hero-text">
                    Analyze • Predict • Prevent • Monitor • Improve Patient Care
                </div>
                <span class="hero-badge">📊 Data Analytics</span>
                <span class="hero-badge">🤖 Machine Learning</span>
                <span class="hero-badge">🚨 Risk Prediction</span>
                <span class="hero-badge">📈 Interactive Dashboard</span>
            </div>
        </div>
        """
    )

    st.markdown(html_content, unsafe_allow_html=True)