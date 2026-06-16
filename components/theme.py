import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_css():
    css_file = BASE_DIR / "style.css"

    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )