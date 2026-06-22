import plotly.graph_objects as go


def apply_plotly_theme(fig: go.Figure):
    """
    Apply a premium dark theme to Plotly charts.
    """

    fig.update_layout(
        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        # Set unified font to match style.css (Inter, SF Pro Display, etc.)
        font=dict(
            family="'Inter', 'SF Pro Display', -apple-system, sans-serif",
            size=13,
            color="#cbd5e1"  # Slate-300 for readable labels
        ),

        # Custom Premium SaaS color palette sequence
        colorway=[
            "#38bdf8",  # Sky-400 (Cyan accent)
            "#60a5fa",  # Blue-400
            "#34d399",  # Emerald-400
            "#fbbf24",  # Amber-400
            "#f87171",  # Red-400
            "#c084fc",  # Purple-400
            "#f472b6",  # Pink-400
            "#2dd4bf"   # Teal-400
        ],

        title=dict(
            font=dict(
                family="'Inter', 'SF Pro Display', -apple-system, sans-serif",
                size=18,
                color="#ffffff"
            ),
            x=0.02,
            xanchor="left"
        ),

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="#e2e8f0", size=12)
        ),

        hoverlabel=dict(
            bgcolor="#0b2133",
            bordercolor="rgba(255,255,255,0.1)",
            font_size=13,
            font_color="#ffffff",
            font_family="'Inter', 'SF Pro Display', -apple-system, sans-serif"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(color="#94a3b8", size=11),
        title_font=dict(color="#cbd5e1", size=12)
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        zeroline=False,
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(color="#94a3b8", size=11),
        title_font=dict(color="#cbd5e1", size=12)
    )

    return fig