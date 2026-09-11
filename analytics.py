"""
AeroGuardian AI - Aviation Analytics Module

Generates interactive Plotly visualizations based strictly on REAL received
aircraft telemetry, weather observations, and prioritized alerts.
No simulated or randomized charts.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import meters_to_feet, ms_to_knots, ms_to_ft_per_min

# Aerospace Dark Palette Tokens
BG_COLOR = "#0f172a"
CARD_BG = "#1e293b"
GRID_COLOR = "#334155"
TEXT_COLOR = "#f8fafc"
CYAN = "#00e5ff"
AMBER = "#f59e0b"
RED = "#ef4444"
GREEN = "#10b981"
PURPLE = "#8b5cf6"


def apply_aerospace_theme(fig: go.Figure, title: str = "") -> go.Figure:
    """Applies a high-contrast modern aerospace control room theme to a Plotly figure."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(color=TEXT_COLOR, size=14, family="Roboto, Inter, sans-serif"),
            x=0.02,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(color="#94a3b8", family="Roboto, Inter, sans-serif", size=12),
        margin=dict(l=30, r=20, t=45, b=30),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showline=True,
            linecolor=GRID_COLOR,
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showline=True,
            linecolor=GRID_COLOR,
        ),
        legend=dict(
            font=dict(color=TEXT_COLOR),
            bgcolor="rgba(30, 41, 59, 0.7)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
        ),
    )
    return fig


def plot_altitude_distribution(df: pd.DataFrame) -> Optional[go.Figure]:
    """Histogram of real aircraft barometric altitudes in feet."""
    if df.empty or "baro_altitude" not in df.columns:
        return None

    valid_alt = df["baro_altitude"].dropna()
    if valid_alt.empty:
        return None

    alt_ft = valid_alt.apply(meters_to_feet) / 1000.0  # In thousands of feet (FL / 10)

    fig = px.histogram(
        x=alt_ft,
        nbins=25,
        labels={"x": "Altitude (x1,000 ft / FL÷10)", "y": "Aircraft Count"},
        color_discrete_sequence=[CYAN],
    )
    fig.update_traces(marker_line_width=1, marker_line_color="#0284c7", opacity=0.85)
    return apply_aerospace_theme(fig, "Altitude Distribution (FL)")


def plot_speed_distribution(df: pd.DataFrame) -> Optional[go.Figure]:
    """Histogram of real aircraft ground speeds in knots."""
    if df.empty or "velocity" not in df.columns:
        return None

    valid_vel = df["velocity"].dropna()
    if valid_vel.empty:
        return None

    speed_kts = valid_vel.apply(ms_to_knots)

    fig = px.histogram(
        x=speed_kts,
        nbins=25,
        labels={"x": "Ground Speed (knots)", "y": "Aircraft Count"},
        color_discrete_sequence=[PURPLE],
    )
    fig.update_traces(marker_line_width=1, marker_line_color="#6d28d9", opacity=0.85)
    return apply_aerospace_theme(fig, "Ground Speed Distribution (knots)")


def plot_country_distribution(df: pd.DataFrame, top_n: int = 10) -> Optional[go.Figure]:
    """Bar chart of aircraft by country of registration."""
    if df.empty or "country" not in df.columns:
        return None

    counts = df["country"].value_counts().head(top_n).reset_index()
    counts.columns = ["Country", "Count"]

    fig = px.bar(
        counts,
        x="Count",
        y="Country",
        orientation="h",
        labels={"Count": "Active Aircraft", "Country": "Country of Registration"},
        color="Count",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    return apply_aerospace_theme(fig, f"Top {top_n} Countries of Registration")


def plot_airborne_ratio(df: pd.DataFrame) -> Optional[go.Figure]:
    """Donut chart showing Airborne vs On-Ground distribution."""
    if df.empty or "on_ground" not in df.columns:
        return None

    status_counts = df["on_ground"].value_counts()
    airborne = status_counts.get(False, 0)
    ground = status_counts.get(True, 0)

    labels = ["Airborne", "On Ground"]
    values = [airborne, ground]
    colors = [CYAN, "#64748b"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color=BG_COLOR, width=2)),
                textinfo="label+percent",
                hoverinfo="label+value+percent",
            )
        ]
    )
    return apply_aerospace_theme(fig, "Airborne vs On-Ground Ratio")


def plot_alert_priority_distribution(alerts: List[Dict[str, Any]]) -> Optional[go.Figure]:
    """Bar chart of prioritized active alerts."""
    if not alerts:
        return None

    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for a in alerts:
        p = a.get("priority", "LOW").upper()
        if p in counts:
            counts[p] += 1

    categories = list(counts.keys())
    values = list(counts.values())
    colors = [RED, AMBER, "#fbbf24", GREEN]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values,
                marker=dict(color=colors, line=dict(color="#1e293b", width=1)),
                text=values,
                textposition="auto",
            )
        ]
    )
    return apply_aerospace_theme(fig, "Alert Priority Breakdown")


def plot_vertical_flight_profile(df: pd.DataFrame) -> Optional[go.Figure]:
    """Pie breakdown of Climbing, Descending, and Level flight states."""
    if df.empty or "vertical_rate" not in df.columns:
        return None

    airborne = df[df["on_ground"] == False]
    if airborne.empty:
        return None

    rates = airborne["vertical_rate"].dropna().apply(ms_to_ft_per_min)
    climbing = (rates > 300).sum()
    descending = (rates < -300).sum()
    level = len(rates) - climbing - descending

    labels = ["Climbing (>300 fpm)", "Level Flight", "Descending (<-300 fpm)"]
    values = [climbing, level, descending]
    colors = [GREEN, CYAN, AMBER]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=colors, line=dict(color=BG_COLOR, width=2)),
                textinfo="label+percent",
            )
        ]
    )
    return apply_aerospace_theme(fig, "Vertical Profile Distribution")


def plot_weather_station_categories(weather_reports: List[Dict[str, Any]]) -> Optional[go.Figure]:
    """Bar chart showing flight categories (VFR, MVFR, IFR, LIFR) of monitored stations."""
    if not weather_reports:
        return None

    counts = {"VFR": 0, "MVFR": 0, "IFR": 0, "LIFR": 0}
    for w in weather_reports:
        c = w.get("flight_category", "VFR").upper()
        if c in counts:
            counts[c] += 1

    categories = list(counts.keys())
    values = list(counts.values())
    colors = [GREEN, CYAN, AMBER, RED]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values,
                marker=dict(color=colors),
                text=values,
                textposition="auto",
            )
        ]
    )
    return apply_aerospace_theme(fig, "Monitored Stations Flight Categories")


def plot_workload_gauge(workload_index: float, level: str) -> go.Figure:
    """Gauge indicator for Pilot Workload & Information Overload (Research Prototype)."""
    color = GREEN
    if workload_index >= 75:
        color = RED
    elif workload_index >= 50:
        color = AMBER
    elif workload_index >= 28:
        color = "#fbbf24"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=workload_index,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": f"<b>Workload Index: {level}</b><br><span style='font-size:11px;color:#94a3b8'>Research Prototype</span>", "font": {"size": 15, "color": TEXT_COLOR}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": GRID_COLOR, "tickfont": {"color": "#94a3b8"}},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "rgba(30, 41, 59, 0.5)",
                "borderwidth": 1,
                "bordercolor": GRID_COLOR,
                "steps": [
                    {"range": [0, 28], "color": "rgba(16, 185, 129, 0.15)"},
                    {"range": [28, 50], "color": "rgba(251, 191, 36, 0.15)"},
                    {"range": [50, 75], "color": "rgba(245, 158, 11, 0.2)"},
                    {"range": [75, 100], "color": "rgba(239, 68, 68, 0.25)"},
                ],
                "threshold": {
                    "line": {"color": RED, "width": 3},
                    "thickness": 0.8,
                    "value": 75,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_COLOR, "family": "Roboto, sans-serif"},
        height=260,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def plot_workload_factors_radar(contributing_factors: List[Dict[str, Any]]) -> go.Figure:
    """Radar chart showing breakdown of workload factors."""
    categories = [f["factor"] for f in contributing_factors]
    values = [f["score"] for f in contributing_factors]

    # Close the radar loop
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            fillcolor="rgba(0, 229, 255, 0.2)",
            line=dict(color=CYAN, width=2),
            marker=dict(color=CYAN, size=6),
            name="Factor Contribution",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor=GRID_COLOR,
                tickfont=dict(color="#94a3b8", size=9),
            ),
            angularaxis=dict(
                gridcolor=GRID_COLOR,
                linecolor=GRID_COLOR,
                tickfont=dict(color=TEXT_COLOR, size=11),
            ),
            bgcolor="rgba(15, 23, 42, 0.5)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=30, b=30),
        height=280,
        showlegend=False,
    )
    return fig
