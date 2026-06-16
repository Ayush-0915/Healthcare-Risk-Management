import plotly.graph_objects as go


def apply_plotly_theme(fig: go.Figure):
    """
    Apply a premium dark theme to Plotly charts.
    """

    fig.update_layout(
        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            size=14,
            color="white"
        ),

        title=dict(
            font=dict(
                size=22,
                color="white"
            ),
            x=0.02,
            xanchor="left"
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="white")
        ),

        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=14,
            font_color="white"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(255,255,255,0.15)",
        tickfont=dict(color="white")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        tickfont=dict(color="white")
    )

    return fig