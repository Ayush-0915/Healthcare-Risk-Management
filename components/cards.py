import streamlit as st
import textwrap


def kpi_card(
    title: str,
    value,
    icon: str = "📊",
    subtitle: str = "",
    color: str = "#2563EB",
):
    """
    Display a modern KPI card.

    Parameters
    ----------
    title : str
        Card title
    value : Any
        Main KPI value
    icon : str
        Emoji or icon
    subtitle : str
        Small helper text
    color : str
        Top border color
    """

    html = textwrap.dedent(
        f"""
        <div class="kpi-card" style="border-top: 5px solid {color};">
            <div class="kpi-card-icon">{icon}</div>
            <div class="kpi-card-value">{value}</div>
            <div class="kpi-card-title">{title}</div>
            <div class="kpi-card-subtitle">{subtitle}</div>
        </div>
        """
    )

    st.markdown(html, unsafe_allow_html=True)


def info_card(
    title: str,
    content: str,
    icon: str = "ℹ️",
):
    """
    Display an informational card.
    """

    html = textwrap.dedent(
        f"""
        <div class="info-card">
            <h3>{icon} {title}</h3>
            <p>{content}</p>
        </div>
        """
    )

    st.markdown(html, unsafe_allow_html=True)


def stat_badge(
    label: str,
    value,
    color: str = "#10B981",
):
    """
    Small pill-shaped badge.
    """

    html = textwrap.dedent(
        f"""
        <span class="stat-badge" style="background-color: {color};">
            {label}: {value}
        </span>
        """
    )

    st.markdown(html, unsafe_allow_html=True)