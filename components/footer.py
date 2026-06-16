import streamlit as st
import textwrap


def show_footer():
    st.markdown("---")

    html = textwrap.dedent(
        """
        <div class="footer-container">
            <div class="footer-title">🏥 Healthcare Risk Management Analytics System</div>
            <div class="footer-text">
                Built with ❤️ using Python, Streamlit, Plotly and Scikit-learn
            </div>
            <div class="footer-text">
                Developed by <b>Ayush Singh</b> | AI/ML Engineer & Data Analyst
            </div>
        </div>
        """
    )

    st.markdown(html, unsafe_allow_html=True)