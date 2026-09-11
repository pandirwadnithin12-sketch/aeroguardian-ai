"""
AeroGuardian AI - An AI Agent for Pilot Workload & Decision Support
Main Theme: "Smart Systems for a Safer Future in Aviation"

Academic & Research Prototype. Strictly real-world aviation data:
- OpenSky Network API (Real-time aircraft state vectors)
- NOAA Aviation Weather Center Data API (Real METAR, TAF)
- OpenAI API / Grounded Heuristic Engine (Explainable AI decision support)

NO SIMULATION POLICY: Missing data is strictly displayed as 'N/A' and never fabricated.
"""

import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Internal application modules
from opensky_client import (
    get_live_aircraft,
    get_live_aircraft_by_region,
    get_opensky_status,
    REGION_BOUNDS,
)
from weather_client import (
    get_metar,
    get_taf,
    get_weather_overview,
    get_weather_status,
    POPULAR_AIRPORTS,
)
from risk_engine import evaluate_airspace_risks, evaluate_aircraft_risk
from alert_manager import AlertManager
from ai_agent import AIGuardianAgent
from flight_routes import resolve_flight_route
from analytics import (
    plot_altitude_distribution,
    plot_speed_distribution,
    plot_country_distribution,
    plot_airborne_ratio,
    plot_vertical_flight_profile,
    plot_alert_priority_distribution,
    plot_weather_station_categories,
    plot_workload_gauge,
    plot_workload_factors_radar,
)
from utils import (
    meters_to_feet,
    ms_to_knots,
    ms_to_ft_per_min,
    hpa_to_inhg,
    fmt_val,
    fmt_altitude,
    fmt_speed,
    fmt_vertical_rate,
    fmt_heading,
    fmt_squawk,
    get_severity_badge_html,
    get_flight_category_badge_html,
)

load_dotenv()

# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AeroGuardian AI | Pilot Workload & Decision Support",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# MODERN AEROSPACE DARK THEME STYLING
# ============================================================

st.markdown(
    """
<style>
/* Base Dark Theme Overrides */
.stApp {
    background-color: #0b0f19;
    color: #f1f5f9;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
}

/* Aerospace Glass Cards */
.aero-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    margin-bottom: 16px;
    backdrop-filter: blur(8px);
}

.aero-card-highlight {
    background: linear-gradient(135deg, rgba(14, 116, 144, 0.2) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(14, 165, 233, 0.4);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 0 20px rgba(14, 165, 233, 0.15);
    margin-bottom: 16px;
}

/* KPI Card Styles */
.kpi-container {
    background: linear-gradient(145deg, #131d31 0%, #0d1527 100%);
    border: 1px solid #1e293b;
    border-top: 2px solid #00e5ff;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
    min-height: 110px;
}

.kpi-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 4px;
    letter-spacing: -0.5px;
}

.kpi-sub {
    font-size: 12px;
    color: #38bdf8;
    margin-top: 4px;
    font-weight: 500;
}

/* Status Indicator Pills */
.status-pill-ok {
    display: inline-flex;
    align-items: center;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.5);
    color: #34d399;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}

.status-pill-warn {
    display: inline-flex;
    align-items: center;
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.5);
    color: #fbbf24;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}

.status-pill-error {
    display: inline-flex;
    align-items: center;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.5);
    color: #f87171;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}

/* Alert Row Styling */
.alert-box-critical {
    background: rgba(239, 68, 68, 0.12);
    border-left: 5px solid #ef4444;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
}

.alert-box-high {
    background: rgba(245, 158, 11, 0.12);
    border-left: 5px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
}

.alert-box-medium {
    background: rgba(251, 191, 36, 0.10);
    border-left: 5px solid #fbbf24;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
}

.alert-box-low {
    background: rgba(56, 189, 248, 0.10);
    border-left: 5px solid #38bdf8;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
}

/* Academic Disclaimer Banner */
.disclaimer-banner {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid #334155;
    border-left: 4px solid #00e5ff;
    padding: 10px 16px;
    border-radius: 6px;
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 18px;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #070b13;
    border-right: 1px solid #1e293b;
}

/* Streamlit Button Accent */
button[kind="primary"] {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

button[kind="secondary"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #f1f5f9 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "alert_manager" not in st.session_state:
    st.session_state.alert_manager = AlertManager()

if "ai_agent" not in st.session_state:
    st.session_state.ai_agent = AIGuardianAgent()

if "aircraft_data" not in st.session_state:
    st.session_state.aircraft_data = []

if "weather_data" not in st.session_state:
    st.session_state.weather_data = []

if "active_alerts" not in st.session_state:
    st.session_state.active_alerts = []

if "workload_info" not in st.session_state:
    st.session_state.workload_info = {}

if "situation_summary" not in st.session_state:
    st.session_state.situation_summary = {}

if "last_refresh_time" not in st.session_state:
    st.session_state.last_refresh_time = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "selected_aircraft_id" not in st.session_state:
    st.session_state.selected_aircraft_id = None

if "monitored_region" not in st.session_state:
    st.session_state.monitored_region = "India"


# ============================================================
# DATA PIPELINE REFRESH FUNCTION
# ============================================================

def refresh_operational_data(force: bool = False):
    """
    Executes real data pipeline:
    1. Fetch live aircraft from OpenSky Network
    2. Fetch live terminal weather from NOAA AWC
    3. Run Risk Identification Engine
    4. Sync with Alert Manager
    5. Calculate Workload Indicator & Situation Awareness
    """
    with st.spinner("Connecting to OpenSky Network & NOAA Weather Center..."):
        # 1. Fetch Aircraft
        try:
            region = st.session_state.monitored_region
            aircraft = get_live_aircraft_by_region(region, force_refresh=force)
            for plane in aircraft:
                plane["route"] = resolve_flight_route(plane)
            st.session_state.aircraft_data = aircraft
        except Exception as e:
            st.warning(f"OpenSky Network status: {e}")
            aircraft = st.session_state.aircraft_data

        # 2. Fetch Terminal Weather
        try:
            weather_reports = get_weather_overview(
                ["VIDP", "VOBL", "VABB", "VOHS", "VECC", "VOMM"]
            )
            st.session_state.weather_data = weather_reports
        except Exception as e:
            st.warning(f"NOAA Aviation Weather status: {e}")
            weather_reports = st.session_state.weather_data

        # 3. Evaluate Airspace Risks
        evaluated_alerts = evaluate_airspace_risks(aircraft, weather_reports)

        # 4. Sync Alert Manager
        st.session_state.active_alerts = st.session_state.alert_manager.sync_alerts(
            evaluated_alerts
        )

        # 5. Calculate AI Workload & Situation Awareness
        workload = st.session_state.ai_agent.calculate_workload_indicator(
            aircraft, st.session_state.active_alerts, weather_reports
        )
        st.session_state.workload_info = workload

        summary = st.session_state.ai_agent.generate_situation_summary(
            aircraft, st.session_state.active_alerts, weather_reports
        )
        st.session_state.situation_summary = summary

        st.session_state.last_refresh_time = datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )


# Initial load if state is empty
if not st.session_state.aircraft_data:
    refresh_operational_data(force=False)


# ============================================================
# SIDEBAR NAVIGATION & SYSTEM CONTROLS
# ============================================================

with st.sidebar:
    st.markdown("## 🛡️ **AeroGuardian AI**")
    st.caption("Human-Factor Guardian & Pilot Decision Support")

    st.markdown(
        """
        <div style="background:#0f172a; border-left: 3px solid #00e5ff; padding: 8px 12px; border-radius: 4px; font-size: 11px; margin-bottom: 12px;">
        <b>Theme:</b> Smart Systems for a Safer Future in Aviation<br>
        <b>Type:</b> Academic Decision Support Prototype
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Main Navigation
    navigation_options = [
        "0. Welcome & Mission",
        "1. Mission Dashboard",
        "2. Live Aircraft",
        "3. Aviation Weather",
        "4. AI Guardian",
        "5. Workload Analysis",
        "6. Alert Center",
        "7. Analytics",
        "8. AI Assistant",
        "9. About",
    ]

    selected_nav = st.radio("System Navigation", navigation_options, index=0)

    st.divider()

    # Region Selection
    st.markdown("### 🌐 Airspace Region")
    region_options = list(REGION_BOUNDS.keys())
    current_region_idx = region_options.index(st.session_state.monitored_region) if st.session_state.monitored_region in region_options else 0
    chosen_region = st.selectbox(
        "Monitored Airspace",
        region_options,
        index=current_region_idx,
        help="Select bounding box for real-time OpenSky queries."
    )

    if chosen_region != st.session_state.monitored_region:
        st.session_state.monitored_region = chosen_region
        refresh_operational_data(force=True)
        st.rerun()

    # Manual Refresh
    if st.button("🔄 Refresh Real Data", type="primary", use_container_width=True):
        refresh_operational_data(force=True)
        st.success("Real-time data refreshed.")
        st.rerun()

    if st.session_state.last_refresh_time:
        st.caption(f"Last update: {st.session_state.last_refresh_time}")

    st.divider()

    # System Status Indicators
    st.markdown("### 📡 External Data Feeds")
    sky_status = get_opensky_status()
    wx_status = get_weather_status()

    if sky_status["is_connected"]:
        st.markdown(
            f'<div class="status-pill-ok">● OpenSky Network: Connected ({sky_status["count"]} acft)</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-pill-warn">● OpenSky Network: Offline / Cached</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    if wx_status["is_connected"]:
        st.markdown(
            f'<div class="status-pill-ok">● NOAA Weather: Connected ({wx_status["stations_monitored_count"]} stns)</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-pill-warn">● NOAA Weather: Checking</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    if st.session_state.ai_agent.client:
        st.markdown(
            f'<div class="status-pill-ok">● AI Engine: OpenAI Active ({st.session_state.ai_agent.model_name})</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-pill-ok">● AI Engine: Context Heuristics Active</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # Academic Disclaimer in Sidebar
    st.caption(
        "⚠️ **Research Prototype**: For educational and decision-support research. "
        "Not certified avionics. Never directly controls aircraft or replaces pilots/ATC."
    )


# ============================================================
# TOP HEADER BAR & PERMANENT SAFETY DISCLAIMER
# ============================================================

col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("✈️ AeroGuardian AI")
    st.markdown(
        "<p style='color:#38bdf8; font-size:16px; margin-top:-14px; font-weight:600;'>"
        "An AI Agent for Pilot Workload & Decision Support "
        "<span style='color:#94a3b8; font-weight:400;'>• Smart Systems for a Safer Future in Aviation</span></p>",
        unsafe_allow_html=True,
    )

with col_h2:
    st.markdown(
        f"""
        <div style="text-align:right; padding-top:10px;">
            <span class="status-pill-ok">LIVE DATA FEED</span>
            <div style="font-size:11px; color:#94a3b8; margin-top:4px;">Airspace: <b>{st.session_state.monitored_region}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Prominent Academic Safety Disclaimer
st.markdown(
    """
    <div class="disclaimer-banner">
        ⚖️ <b>SAFETY & ACADEMIC DISCLAIMER:</b> AeroGuardian AI is a research and educational decision-support prototype.
        It is not certified aviation software and must not be used for aircraft control, flight-critical decisions, or operational aviation.
        All AI observations use cautious phrasing (<i>'Potential concern detected'</i>, <i>'Further verification recommended'</i>) and never command aircraft actions.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION VIEW 0: WELCOME & MISSION OVERVIEW
# ============================================================

if selected_nav == "0. Welcome & Mission":
    st.markdown("### 🛡️ Welcome to AeroGuardian AI")

    # Hero Card
    st.markdown(
        """
        <div class="aero-card-highlight">
            <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(0,229,255,0.15);border:1px solid rgba(0,229,255,0.4);color:#00e5ff;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">
                AEROGUARDIAN AI v3.2 • HUMAN-FACTOR FLIGHT SAFETY
            </div>
            <h2 style="color:#ffffff;font-size:26px;font-weight:800;margin:0 0 10px 0;letter-spacing:-0.5px;">
                Next-Generation Airspace Guardian &amp; Pilot Decision Support
            </h2>
            <p style="color:#cbd5e1;font-size:14px;line-height:1.6;margin-bottom:16px;">
                Welcome to <b>AeroGuardian AI</b> — an intelligent aeronautical decision-support system designed to mitigate pilot and air traffic controller cognitive overload. Fusing real-time Mode-S / ADS-B transponder telemetry with official NOAA Aviation Weather observations, AeroGuardian AI delivers continuous conflict prediction, situational awareness, and intelligent human-factor safety guardrails.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    aircraft = st.session_state.aircraft_data
    alerts = st.session_state.active_alerts
    weather_reports = st.session_state.weather_data
    workload = st.session_state.workload_info

    total_acft = len(aircraft)
    airborne_acft = sum(1 for p in aircraft if not p.get("on_ground", False))
    crit_alerts = sum(1 for a in alerts if a.get("priority") == "CRITICAL")
    wl_score = workload.get("workload_index", 0)
    wl_level = workload.get("level", "LOW")

    # Airspace Readiness Metrics Strip
    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Live Aircraft</div>
                <div class="kpi-value">{total_acft}</div>
                <div class="kpi-sub">{st.session_state.monitored_region} Airspace</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with w2:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Airborne Transponders</div>
                <div class="kpi-value">{airborne_acft}</div>
                <div class="kpi-sub">{total_acft - airborne_acft} On Ground</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with w3:
        st.markdown(
            f"""
            <div class="kpi-container" style="border-top-color: {'#ff3366' if crit_alerts > 0 else '#f59e0b'};">
                <div class="kpi-title">Active Alerts</div>
                <div class="kpi-value" style="color: {'#ff3366' if crit_alerts > 0 else '#f8fafc'};">{len(alerts)}</div>
                <div class="kpi-sub">{crit_alerts} Critical Alerts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with w4:
        st.markdown(
            f"""
            <div class="kpi-container" style="border-top-color: {'#ff3366' if wl_score >= 75 else '#f59e0b' if wl_score >= 50 else '#00e5ff'};">
                <div class="kpi-title">Workload Index</div>
                <div class="kpi-value">{wl_score}%</div>
                <div class="kpi-sub">{wl_level} Saturation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Core Capabilities & Interactive Modules
    st.markdown("#### 🧭 Core Aerospace Modules &amp; Capabilities")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            """
            <div class="aero-card" style="height: 190px;">
                <h4 style="color:#00e5ff;margin-top:0;">🎛️ Mission Dashboard</h4>
                <p style="color:#94a3b8;font-size:13px;line-height:1.5;">
                    Tactical radar visualization with heading vectors, dynamic aircraft interpolation, conflict proximity warnings, and multi-layer custom map basemaps.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="aero-card" style="height: 190px;">
                <h4 style="color:#00e5ff;margin-top:0;">✈️ Live Mode-S Telemetry</h4>
                <p style="color:#94a3b8;font-size:13px;line-height:1.5;">
                    Deep flight state vectors including Mach numbers, vertical climb/descent rates, barometric altitudes, squawk codes, flight phases, and CSV export.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="aero-card" style="height: 190px;">
                <h4 style="color:#00e5ff;margin-top:0;">🌦️ Aviation Weather</h4>
                <p style="color:#94a3b8;font-size:13px;line-height:1.5;">
                    Official NOAA Aviation Weather Center terminal aerodrome reports, flight categories (VFR/MVFR/IFR/LIFR), altimeter settings, and wind vectors.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    m4, m5, m6 = st.columns(3)
    with m4:
        st.markdown(
            """
            <div class="aero-card" style="height: 190px;">
                <h4 style="color:#00e5ff;margin-top:0;">🛡️ AI Guardian Reasoning</h4>
                <p style="color:#94a3b8;font-size:13px;line-height:1.5;">
                    Autonomous natural-language situational report evaluating airspace density, adverse weather intersections, and cognitive overload risk factors.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m5:
        st.markdown(
            """
            <div class="aero-card" style="height: 190px;">
                <h4 style="color:#00e5ff;margin-top:0;">📊 Cognitive Workload Model</h4>
                <p style="color:#94a3b8;font-size:13px;line-height:1.5;">
                    Human-factors cognitive saturation model computing aircraft volume, maneuvering transitions, adverse weather stress, and alert frequencies.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m6:
        st.markdown(
            """
            <div class="aero-card" style="height: 190px;">
                <h4 style="color:#00e5ff;margin-top:0;">🤖 AI Aviation Copilot</h4>
                <p style="color:#94a3b8;font-size:13px;line-height:1.5;">
                    Interactive conversational assistant grounded in real-time telemetry, aerodynamic principles, standard ATC phraseology, and flight regulations.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 3-Step Decision Support Pipeline
    st.markdown("#### 📡 How AeroGuardian AI Safeguards Airspace")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            """
            <div class="aero-card">
                <div style="font-size:24px;font-weight:900;color:rgba(0,229,255,0.4);font-family:monospace;">01</div>
                <h4 style="color:#fff;margin:6px 0;">Telemetry &amp; Weather Ingestion</h4>
                <p style="color:#94a3b8;font-size:12px;line-height:1.5;">
                    Continuous ingest of real-time OpenSky Network ADS-B transponder state vectors coupled with live NOAA Aviation Weather Center aerodrome reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            """
            <div class="aero-card">
                <div style="font-size:24px;font-weight:900;color:rgba(0,229,255,0.4);font-family:monospace;">02</div>
                <h4 style="color:#fff;margin:6px 0;">Multi-Layer Risk &amp; Conflict Fusion</h4>
                <p style="color:#94a3b8;font-size:12px;line-height:1.5;">
                    Automated calculations for horizontal &amp; vertical separation loss, excessive climb/descent rates, emergency squawk codes (7700/7600/7500), and convective weather hazards.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            """
            <div class="aero-card">
                <div style="font-size:24px;font-weight:900;color:rgba(0,229,255,0.4);font-family:monospace;">03</div>
                <h4 style="color:#fff;margin:6px 0;">Human-Centered Decision Support</h4>
                <p style="color:#94a3b8;font-size:12px;line-height:1.5;">
                    Prioritized cognitive alerts and plain-language situation digests designed to augment pilot and air traffic controller decision-making without overriding human authority.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

# ============================================================
# NAVIGATION VIEW 1: MISSION DASHBOARD
# ============================================================

if selected_nav == "1. Mission Dashboard":
    st.markdown("### 🎛️ Mission Dashboard")

    aircraft = st.session_state.aircraft_data
    alerts = st.session_state.active_alerts
    weather_reports = st.session_state.weather_data
    workload = st.session_state.workload_info
    summary = st.session_state.situation_summary

    total_acft = len(aircraft)
    airborne_acft = sum(1 for p in aircraft if not p.get("on_ground", False))
    crit_count = sum(1 for a in alerts if a.get("priority") == "CRITICAL")
    high_count = sum(1 for a in alerts if a.get("priority") == "HIGH")
    attention_count = len(alerts)
    weather_stns = len(weather_reports)
    wl_score = workload.get("workload_index", 0)
    wl_level = workload.get("level", "LOW")

    # 1. Top KPI Row
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Live Aircraft</div>
                <div class="kpi-value">{total_acft}</div>
                <div class="kpi-sub">{st.session_state.monitored_region} Airspace</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Airborne Flights</div>
                <div class="kpi-value">{airborne_acft}</div>
                <div class="kpi-sub">{total_acft - airborne_acft} on ground</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-container" style="border-top:2px solid {'#ff3366' if crit_count > 0 else '#ff9900' if high_count > 0 else '#00d4aa'};">
                <div class="kpi-title">Attention Items</div>
                <div class="kpi-value">{attention_count}</div>
                <div class="kpi-sub">{crit_count} Crit • {high_count} High</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Weather Stations</div>
                <div class="kpi-value">{weather_stns}</div>
                <div class="kpi-sub">NOAA Real-time METAR</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k5:
        wl_color = "#ff3366" if wl_score >= 75 else "#ff9900" if wl_score >= 50 else "#00e5ff"
        st.markdown(
            f"""
            <div class="kpi-container" style="border-top:2px solid {wl_color};">
                <div class="kpi-title">Workload Indicator</div>
                <div class="kpi-value" style="color:{wl_color};">{wl_score}%</div>
                <div class="kpi-sub">{wl_level} Level (Research)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 2. Main Middle Row: Live Map (Left) & AI Situation Awareness (Right)
    map_col, ai_col = st.columns([7, 5])

    with map_col:
        st.markdown("#### 🌍 Real-Time Aircraft Radar Map")

        pos_aircraft = [
            p for p in aircraft
            if p.get("latitude") is not None and p.get("longitude") is not None
        ]

        if pos_aircraft:
            df_pos = pd.DataFrame(pos_aircraft)
            df_pos["alt_ft"] = df_pos["baro_altitude"].apply(lambda x: int(meters_to_feet(x)) if x is not None else 0)
            df_pos["spd_kts"] = df_pos["velocity"].apply(lambda x: int(ms_to_knots(x)) if x is not None else 0)

            # Mark attention status for colors
            alert_icaos = {a["icao24"] for a in alerts}
            crit_icaos = {a["icao24"] for a in alerts if a["priority"] == "CRITICAL"}
            high_icaos = {a["icao24"] for a in alerts if a["priority"] == "HIGH"}

            def get_status_label(row):
                i = row["icao24"]
                if i in crit_icaos:
                    return "Critical Attention"
                elif i in high_icaos:
                    return "High Attention"
                elif i in alert_icaos:
                    return "Monitored Attention"
                elif row["on_ground"]:
                    return "On Ground"
                return "Nominal Airborne"

            df_pos["status"] = df_pos.apply(get_status_label, axis=1)

            color_map = {
                "Critical Attention": "#ff3366",
                "High Attention": "#f59e0b",
                "Monitored Attention": "#fbbf24",
                "Nominal Airborne": "#00e5ff",
                "On Ground": "#64748b",
            }

            # Choose map center based on region
            center_lat, center_lon, zoom = 22.0, 79.0, 4.0
            if st.session_state.monitored_region == "Global":
                center_lat, center_lon, zoom = 20.0, 0.0, 1.2
            elif st.session_state.monitored_region == "Europe":
                center_lat, center_lon, zoom = 50.0, 10.0, 3.5
            elif st.session_state.monitored_region == "North America":
                center_lat, center_lon, zoom = 39.0, -98.0, 3.2

            fig_map = px.scatter_mapbox(
                df_pos,
                lat="latitude",
                lon="longitude",
                color="status",
                color_discrete_map=color_map,
                hover_name="callsign",
                hover_data={
                    "icao24": True,
                    "country": True,
                    "alt_ft": True,
                    "spd_kts": True,
                    "status": True,
                    "latitude": False,
                    "longitude": False,
                },
                zoom=zoom,
                center={"lat": center_lat, "lon": center_lon},
                mapbox_style="carto-darkmatter",
            )
            fig_map.update_traces(marker=dict(size=8, opacity=0.85))
            fig_map.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0),
                height=480,
                legend=dict(
                    yanchor="bottom",
                    y=0.02,
                    xanchor="left",
                    x=0.02,
                    bgcolor="rgba(15, 23, 42, 0.85)",
                    bordercolor="#334155",
                    borderwidth=1,
                    font=dict(color="#f8fafc", size=10),
                ),
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("No aircraft with valid coordinates found in currently received OpenSky packet.")

    with ai_col:
        st.markdown("#### 🧠 AI Situation Awareness")

        st.markdown(
            f"""
            <div class="aero-card-highlight">
                <div style="font-size:12px; font-weight:700; color:#00e5ff; letter-spacing:1px; text-transform:uppercase;">
                    Current Situation Overview
                </div>
                <div style="font-size:13px; color:#94a3b8; margin-top:4px; margin-bottom:12px;">
                    Airspace: <b>{st.session_state.monitored_region}</b> • 
                    Flights Monitored: <b>{summary.get('aircraft_monitored', 0)}</b> ({summary.get('aircraft_airborne', 0)} airborne) • 
                    Attention Items: <b>{summary.get('active_attention_items', 0)}</b>
                </div>
                <div style="font-size:14px; line-height:1.6; color:#f1f5f9; background:rgba(0,0,0,0.25); padding:12px; border-radius:8px; border-left:3px solid #00e5ff;">
                    "{summary.get('summary_text', 'Generating situation awareness analysis...')}"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Quick Workload Gauge Preview
        st.plotly_chart(
            plot_workload_gauge(wl_score, wl_level),
            use_container_width=True,
        )

    # 3. Bottom Row: Priority Alerts Feed & Live Weather Strip
    st.markdown("#### 🚨 Priority Alerts Feed")

    if alerts:
        display_alerts = alerts[:5]
        for a in display_alerts:
            p = a.get("priority", "LOW")
            box_class = f"alert-box-{p.lower()}"
            badge_html = get_severity_badge_html(p)

            col_a1, col_a2 = st.columns([5, 1])
            with col_a1:
                st.markdown(
                    f"""
                    <div class="{box_class}">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <b>{badge_html} &nbsp; {a['alert_title']}</b>
                            <span style="font-size:11px; color:#94a3b8;">{a['timestamp']}</span>
                        </div>
                        <div style="font-size:13px; color:#f1f5f9; margin-top:6px;">
                            Aircraft: <b>{a['callsign']}</b> (ICAO24: <code>{a['icao24']}</code>) - {a['detected']}
                        </div>
                        <div style="font-size:12px; color:#94a3b8; margin-top:4px;">
                            <b>Trigger Data:</b> {a['triggering_data']} | <b>Suggested Action:</b> {a['suggested_verification']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_a2:
                btn_label = "Unmark" if a.get("acknowledged") else "Acknowledge"
                if st.button(btn_label, key=f"dash_ack_{a['id']}", use_container_width=True):
                    if a.get("acknowledged"):
                        st.session_state.alert_manager.unacknowledge_alert(a["id"])
                    else:
                        st.session_state.alert_manager.acknowledge_alert(a["id"])
                    st.rerun()
    else:
        st.markdown(
            """
            <div class="alert-box-low">
                <b>✅ Nominal Airspace Operations:</b> No priority alerts currently detected.
                All monitored flights are adhering to standard flight levels, velocity corridors, and transponder codes.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Weather Strip
    st.markdown("#### 🌤️ Terminal Weather Snapshot")
    if weather_reports:
        w_cols = st.columns(len(weather_reports[:6]))
        for idx, w in enumerate(weather_reports[:6]):
            with w_cols[idx]:
                cat_badge = get_flight_category_badge_html(w.get("flight_category", "VFR"))
                st.markdown(
                    f"""
                    <div class="aero-card" style="padding:12px; text-align:center;">
                        <div style="font-size:14px; font-weight:800; color:#f8fafc;">{w['icao']}</div>
                        <div style="margin:4px 0;">{cat_badge}</div>
                        <div style="font-size:12px; color:#94a3b8;">Wind: {w.get('wind_speed_kt', 'N/A')} kts</div>
                        <div style="font-size:11px; color:#38bdf8;">Vis: {w.get('visibility_sm', 'N/A')} SM</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================
# NAVIGATION VIEW 2: LIVE AIRCRAFT
# ============================================================

elif selected_nav == "2. Live Aircraft":
    st.markdown("### ✈️ Live Aircraft Tracking & Fleet Diagnostics")
    st.caption("Real-time aircraft state vectors retrieved directly from OpenSky Network.")

    aircraft = st.session_state.aircraft_data
    alerts = st.session_state.active_alerts

    if not aircraft:
        st.warning("No real aircraft data available. Please click 'Refresh Real Data' in the sidebar.")
    else:
        # Search & Filters
        f1, f2, f3 = st.columns([3, 2, 2])
        with f1:
            search_query = st.text_input("🔍 Search by Callsign, ICAO24, or Country", "")
        with f2:
            filter_status = st.selectbox(
                "Flight Status", ["All", "Airborne Only", "On Ground Only", "Attention Items Only"]
            )
        with f3:
            min_speed = st.slider("Min Speed (kts)", 0, 600, 0, 25)

        # Filter logic
        filtered_aircraft = aircraft
        if search_query:
            q = search_query.strip().lower()
            filtered_aircraft = [
                p for p in filtered_aircraft
                if q in p.get("callsign", "").lower()
                or q in p.get("icao24", "").lower()
                or q in p.get("country", "").lower()
            ]

        if filter_status == "Airborne Only":
            filtered_aircraft = [p for p in filtered_aircraft if not p.get("on_ground", False)]
        elif filter_status == "On Ground Only":
            filtered_aircraft = [p for p in filtered_aircraft if p.get("on_ground", False)]
        elif filter_status == "Attention Items Only":
            alert_icaos = {a["icao24"] for a in alerts}
            filtered_aircraft = [p for p in filtered_aircraft if p.get("icao24") in alert_icaos]

        if min_speed > 0:
            filtered_aircraft = [
                p for p in filtered_aircraft
                if p.get("velocity") is not None and ms_to_knots(p["velocity"]) >= min_speed
            ]

        st.markdown(f"**Displaying {len(filtered_aircraft)} of {len(aircraft)} monitored aircraft**")

        # Map & Detail Layout
        col_map, col_detail = st.columns([7, 5])

        with col_map:
            # Aircraft Table
            table_rows = []
            for p in filtered_aircraft:
                alt_str = fmt_altitude(p.get("baro_altitude"), p.get("geo_altitude"))
                spd_str = fmt_speed(p.get("velocity"))
                vr_str = fmt_vertical_rate(p.get("vertical_rate"))
                hdg_str = fmt_heading(p.get("heading"))
                sq_str = fmt_squawk(p.get("squawk"))

                route_obj = p.get("route")
                route_str = route_obj.get("route_code") if route_obj and route_obj.get("has_route") else "En Route"

                table_rows.append(
                    {
                        "Callsign": p.get("callsign") or "N/A",
                        "Route": route_str,
                        "ICAO24": p.get("icao24"),
                        "Country": p.get("country"),
                        "Altitude": alt_str,
                        "Speed": spd_str,
                        "Vertical Rate": vr_str,
                        "Heading": hdg_str,
                        "Squawk": sq_str,
                        "Status": "Ground" if p.get("on_ground") else "Airborne",
                    }
                )

            df_display = pd.DataFrame(table_rows)
            st.dataframe(df_display, use_container_width=True, height=450)

            # Download CSV
            csv = df_display.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Aircraft Telemetry (CSV)",
                data=csv,
                file_name=f"aeroguardian_telemetry_{int(time.time())}.csv",
                mime="text/csv",
            )

        with col_detail:
            st.markdown("#### 🔬 Aircraft Detail & AI Diagnostic Panel")

            # Selection Box
            callsign_options = [
                f"{p.get('callsign') or 'No-Callsign'} ({p.get('icao24')})"
                for p in filtered_aircraft
            ]

            if callsign_options:
                selected_opt = st.selectbox(
                    "Select Aircraft to Inspect",
                    callsign_options,
                    index=0,
                )
                selected_icao = selected_opt.split("(")[-1].replace(")", "").strip()
                selected_plane = next(
                    (p for p in filtered_aircraft if p.get("icao24") == selected_icao),
                    None,
                )

                if selected_plane:
                    # Run AI Diagnostic on this plane
                    diag = st.session_state.ai_agent.analyze_aircraft_detail(
                        selected_plane, alerts, st.session_state.weather_data
                    )

                    sev_badge = get_severity_badge_html(diag["attention_tier"])

                    st.markdown(
                        f"""
                        <div class="aero-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h3 style="margin:0; color:#f8fafc;">✈️ {diag['callsign']}</h3>
                                {sev_badge}
                            </div>
                            <div style="font-size:12px; color:#94a3b8; margin-top:2px;">
                                ICAO24: <code>{diag['icao24']}</code> • Country: <b>{diag['country']}</b>
                            </div>
                            <div style="font-size:13px; color:#38bdf8; margin-top:6px;">
                                Attention Status: <b>{diag['attention_badge']}</b>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Real Flight Route (Start to End)
                    route_info = selected_plane.get("route")
                    if route_info and route_info.get("has_route"):
                        orig = route_info.get("origin", {})
                        dest = route_info.get("destination", {})
                        st.markdown(
                            f"""
                            <div style="background:rgba(15,23,42,0.85); border:1px solid #00e5ff; border-radius:8px; padding:12px; margin-top:10px; margin-bottom:12px;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <div style="text-align:left;">
                                        <div style="font-size:10px; color:#00d4aa; font-weight:800;">🛫 START (ORIGIN)</div>
                                        <div style="font-size:18px; font-weight:bold; color:#fff;">{orig.get('iata', orig.get('code', 'N/A'))}</div>
                                        <div style="font-size:11px; color:#94a3b8;">{orig.get('city', '')}</div>
                                    </div>
                                    <div style="text-align:center; padding:0 12px; flex-grow:1;">
                                        <div style="font-size:12px; color:#00e5ff; font-weight:bold;">{route_info.get('route_code')}</div>
                                        <div style="font-size:11px; color:#cbd5e1;">{round(route_info.get('traveled_km', 0))} km / {round(route_info.get('total_km', 0))} km</div>
                                    </div>
                                    <div style="text-align:right;">
                                        <div style="font-size:10px; color:#ff3366; font-weight:800;">🛬 END (DESTINATION)</div>
                                        <div style="font-size:18px; font-weight:bold; color:#fff;">{dest.get('iata', dest.get('code', 'N/A'))}</div>
                                        <div style="font-size:11px; color:#94a3b8;">{dest.get('city', '')}</div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        prog = min(max(int(route_info.get("progress_pct", 50)), 0), 100)
                        st.progress(prog / 100, text=f"Journey Completed: {route_info.get('progress_pct', 0)}% (Heading {fmt_heading(selected_plane.get('heading'))})")

                    # Telemetry Metrics Grid
                    t1, t2 = st.columns(2)
                    with t1:
                        st.markdown(f"**Altitude:** {fmt_altitude(selected_plane.get('baro_altitude'))}")
                        st.markdown(f"**Speed:** {fmt_speed(selected_plane.get('velocity'))}")
                        st.markdown(f"**Vertical Rate:** {fmt_vertical_rate(selected_plane.get('vertical_rate'))}")
                    with t2:
                        st.markdown(f"**Heading:** {fmt_heading(selected_plane.get('heading'))}")
                        st.markdown(f"**Squawk:** {fmt_squawk(selected_plane.get('squawk'))}")
                        st.markdown(f"**Coordinates:** {fmt_val(selected_plane.get('latitude'), '°N', 3)}, {fmt_val(selected_plane.get('longitude'), '°E', 3)}")

                    st.divider()

                    # Data Quality / Missing Fields Audit
                    st.markdown("##### 📡 Data Quality & Telemetry Audit")
                    completeness = diag["data_completeness_pct"]
                    st.progress(int(completeness) / 100, text=f"Telemetry Completeness: {int(completeness)}%")

                    if diag["missing_fields"]:
                        st.caption(f"Missing transmitted fields: {', '.join(diag['missing_fields'])} (displayed safely as N/A)")
                    else:
                        st.caption("All primary Mode-S / ADS-B state vector fields successfully received.")

                    st.divider()

                    # AI Observations
                    st.markdown("##### 🧠 AI Guardian Observations")
                    for obs in diag["observations"]:
                        badge = get_severity_badge_html(obs["priority"])
                        st.markdown(
                            f"""
                            <div style="background:rgba(15,23,42,0.6); border-left:3px solid #00e5ff; padding:10px 12px; border-radius:6px; margin-bottom:10px;">
                                <b>{badge} {obs['title']}</b>
                                <div style="font-size:12px; color:#e2e8f0; margin-top:4px;"><b>Detected:</b> {obs['what_detected']}</div>
                                <div style="font-size:12px; color:#94a3b8; margin-top:2px;"><b>Why it matters:</b> {obs['why_it_matters']}</div>
                                <div style="font-size:11px; color:#38bdf8; margin-top:4px;"><b>Action:</b> {obs['suggested_action']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.info("No aircraft match the current search filters.")


# ============================================================
# NAVIGATION VIEW 3: AVIATION WEATHER
# ============================================================

elif selected_nav == "3. Aviation Weather":
    st.markdown("### 🌤️ Real Aviation Weather (NOAA Aviation Weather Center)")
    st.caption("Decoded METAR observations, cloud layers, and Terminal Aerodrome Forecasts (TAF).")

    # Airport selection
    col_w1, col_w2 = st.columns([2, 1])
    with col_w1:
        preset_choice = st.selectbox(
            "Select Monitored Airport Preset",
            list(POPULAR_AIRPORTS.keys()),
            format_func=lambda x: f"{x} - {POPULAR_AIRPORTS[x]}",
            index=0,
        )
    with col_w2:
        custom_icao = st.text_input("Or Enter Custom ICAO Station Code", "", max_chars=4).strip().upper()

    station_to_query = custom_icao if (custom_icao and len(custom_icao) == 4) else preset_choice

    # Fetch METAR and TAF
    with st.spinner(f"Querying NOAA AWC for station {station_to_query}..."):
        metar = get_metar(station_to_query)
        taf = get_taf(station_to_query)

    if metar:
        flt_cat = metar.get("flight_category", "UNKNOWN")
        cat_badge = get_flight_category_badge_html(flt_cat)

        st.markdown(
            f"""
            <div class="aero-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 style="margin:0; color:#f8fafc;">{metar['icao']} — {metar['name']}</h2>
                        <span style="font-size:12px; color:#94a3b8;">Report Time: {metar.get('report_time') or 'Latest Available'}</span>
                    </div>
                    <div>{cat_badge}</div>
                </div>
                <div style="font-family:monospace; background:rgba(0,0,0,0.35); padding:10px; border-radius:6px; margin-top:12px; color:#38bdf8; font-size:13px;">
                    {metar['raw_text']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Weather Metrics
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            wind_dir = fmt_val(metar.get("wind_dir_deg"), "°", 0)
            wind_spd = fmt_val(metar.get("wind_speed_kt"), "kts", 0)
            wind_gst = f" (Gusts: {metar['wind_gust_kt']} kts)" if metar.get("wind_gust_kt") else ""
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Wind Vector</div>
                    <div class="kpi-value" style="font-size:20px;">{wind_dir} @ {wind_spd}</div>
                    <div class="kpi-sub">{wind_gst if wind_gst else 'Steady wind'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m2:
            vis_sm = fmt_val(metar.get("visibility_sm"), "SM", 1)
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Visibility</div>
                    <div class="kpi-value" style="font-size:20px;">{vis_sm}</div>
                    <div class="kpi-sub">Conditions: {metar.get('weather_string', 'None')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m3:
            temp_c = fmt_val(metar.get("temperature_c"), "°C", 0)
            dewp_c = fmt_val(metar.get("dewpoint_c"), "°C", 0)
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Temperature / Dewpoint</div>
                    <div class="kpi-value" style="font-size:20px;">{temp_c} / {dewp_c}</div>
                    <div class="kpi-sub">Spread: {fmt_val(metar.get('temp_dewpoint_spread'), '°C')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m4:
            altim_hpa = metar.get("altimeter_hpa")
            altim_str = f"{altim_hpa} hPa" if altim_hpa else "N/A"
            inhg = hpa_to_inhg(altim_hpa)
            inhg_str = f"({inhg:.2f} inHg)" if inhg else ""
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Altimeter (QNH)</div>
                    <div class="kpi-value" style="font-size:20px;">{altim_str}</div>
                    <div class="kpi-sub">{inhg_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Cloud layers breakdown
        col_c1, col_c2 = st.columns([1, 1])

        with col_c1:
            st.markdown("#### ☁️ Cloud Layers & Ceiling")
            clouds = metar.get("clouds") or []
            if clouds:
                for c in clouds:
                    cov = c.get("cover", "NSC")
                    base = c.get("base")
                    c_type = c.get("type", "")
                    base_str = f"{base:,} ft AGL" if base is not None else "Clear of clouds"
                    cb_alert = " ⚠️ Cumulonimbus (CB)" if c_type == "CB" else ""
                    st.markdown(f"- **{cov}**: {base_str}{cb_alert}")
            else:
                st.markdown("- **SKC / CLR**: Clear skies / No significant clouds detected.")

            if metar.get("ceiling_ft"):
                st.markdown(f"**Lowest Ceiling:** `{int(metar['ceiling_ft']):,} ft AGL`")
            else:
                st.markdown("**Ceiling:** Unlimited (VFR compliant)")

        with col_c2:
            st.markdown("#### 📑 Terminal Aerodrome Forecast (TAF)")
            if taf:
                st.caption(f"TAF Issued: {taf.get('issue_time') or 'Recent'}")
                st.markdown(
                    f"""
                    <div style="font-family:monospace; background:rgba(0,0,0,0.35); padding:10px; border-radius:6px; color:#a7f3d0; font-size:12px; max-height:160px; overflow-y:auto;">
                        {taf.get('raw_text')}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("No active TAF forecast issued for this aerodrome.")

    else:
        st.error(
            f"❌ Unable to retrieve real METAR for station '{station_to_query}'. "
            "Verify that the ICAO code is valid and active in the NOAA Aviation Weather database."
        )


# ============================================================
# NAVIGATION VIEW 4: AI GUARDIAN
# ============================================================

elif selected_nav == "4. AI Guardian":
    st.markdown("### 🧠 AI Guardian Agent")
    st.caption("Automated risk identification, explainable reasoning, and human-factor decision support.")

    alerts = st.session_state.active_alerts
    workload = st.session_state.workload_info
    summary = st.session_state.situation_summary

    # Executive Situation Block
    st.markdown(
        f"""
        <div class="aero-card-highlight">
            <h4 style="margin:0 0 8px 0; color:#00e5ff;">AI Guardian Executive Situation Report</h4>
            <div style="font-size:14px; line-height:1.6; color:#f8fafc;">
                {summary.get('summary_text', 'Evaluating real airspace status...')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🚨 Prioritized Attention Items")

    if alerts:
        for idx, a in enumerate(alerts):
            p = a.get("priority", "LOW")
            sev_badge = get_severity_badge_html(p)

            with st.expander(f"{p} — {a['callsign']} ({a['icao24']}): {a['alert_title']}", expanded=(idx < 2)):
                e1, e2 = st.columns([3, 2])
                with e1:
                    st.markdown(f"**What was detected:**\n{a['detected']}")
                    st.markdown(f"**Why it matters:**\n{a['why_it_matters']}")
                with e2:
                    st.markdown(f"**Triggering Telemetry Data:**\n`{a['triggering_data']}`")
                    st.markdown(f"**Confidence Rating:**\n*{a['confidence']}*")
                    st.markdown(f"**Suggested Verification Action:**\n`{a['suggested_verification']}`")

                # Acknowledgment button
                if st.button("Acknowledge Alert", key=f"ai_ack_{a['id']}"):
                    st.session_state.alert_manager.acknowledge_alert(a["id"])
                    st.success("Alert acknowledged.")
                    st.rerun()
    else:
        st.success("✅ Zero active attention items. All flights are operating within nominal parameters.")


# ============================================================
# NAVIGATION VIEW 5: WORKLOAD ANALYSIS
# ============================================================

elif selected_nav == "5. Workload Analysis":
    st.markdown("### ⚡ Pilot Workload & Information Overload Analysis")
    st.caption("AI-Assisted Workload Indicator — Research Prototype")

    workload = st.session_state.workload_info
    wl_score = workload.get("workload_index", 0)
    wl_level = workload.get("level", "LOW")
    wl_desc = workload.get("level_description", "")
    factors = workload.get("contributing_factors", [])

    st.markdown(
        f"""
        <div class="aero-card">
            <div style="font-size:12px; text-transform:uppercase; color:#00e5ff; font-weight:700; letter-spacing:1px;">
                Operational Complexity Assessment
            </div>
            <h2 style="margin:4px 0; color:#f8fafc;">Workload Indicator: {wl_score}% — {wl_level}</h2>
            <div style="font-size:14px; color:#cbd5e1;">{wl_desc}</div>
            <div style="font-size:11px; color:#94a3b8; margin-top:8px;">
                <i>{workload.get('disclaimer', '')}</i>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Charts: Gauge + Radar
    col_g, col_r = st.columns([1, 1])

    with col_g:
        st.markdown("#### ⏱️ Workload Index Gauge")
        st.plotly_chart(plot_workload_gauge(wl_score, wl_level), use_container_width=True)

    with col_r:
        st.markdown("#### 🕸️ Contributing Complexity Factors")
        if factors:
            st.plotly_chart(plot_workload_factors_radar(factors), use_container_width=True)

    # Factors Table
    st.markdown("#### 📊 Transparent Factor Weighting Breakdown")
    factor_rows = []
    for f in factors:
        factor_rows.append(
            {
                "Contributing Factor": f["factor"],
                "Model Weight": f["weight"],
                "Calculated Score (0-100)": f"{f['score']}/100",
                "Observable Telemetry Details": f["details"],
            }
        )
    st.table(pd.DataFrame(factor_rows))

    st.markdown(
        """
        <div style="background:rgba(15,23,42,0.8); border:1px solid #334155; padding:12px; border-radius:8px; font-size:12px; color:#94a3b8;">
            <b>Human Factors Note:</b> In modern glass-cockpit and ATC environments, high information volume during non-nominal events
            can trigger cognitive saturation. AeroGuardian AI synthesizes state vectors and terminal weather into a single structured
            indicator to support situational prioritization without asserting flight-control authority.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# NAVIGATION VIEW 6: ALERT CENTER
# ============================================================

elif selected_nav == "6. Alert Center":
    st.markdown("### 🔔 Intelligent Alert Center & Triage")
    st.caption("Categorized operational alerts with acknowledgment tracking and history.")

    mgr = st.session_state.alert_manager
    counts = mgr.get_severity_counts()

    # Filter Controls
    c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
    with c1:
        pri_filter = st.selectbox("Filter Priority", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    with c2:
        inc_ack = st.checkbox("Show Acknowledged Alerts", value=True)
    with c3:
        search_alert = st.text_input("Search Alerts", "")
    with c4:
        if st.button("Clear Acknowledged", use_container_width=True):
            mgr.clear_acknowledged()
            st.rerun()

    active_alerts = mgr.get_active_alerts(
        priority_filter=pri_filter if pri_filter != "ALL" else None,
        include_acknowledged=inc_ack,
        search_query=search_alert,
    )

    st.markdown(f"**Active Alerts:** {len(active_alerts)} | Critical: {counts['CRITICAL']} | High: {counts['HIGH']} | Medium: {counts['MEDIUM']} | Low: {counts['LOW']}")

    if active_alerts:
        for a in active_alerts:
            p = a.get("priority", "LOW")
            is_ack = a.get("acknowledged", False)
            badge_html = get_severity_badge_html(p)
            ack_tag = "<span style='color:#34d399; font-weight:700;'>[ACKNOWLEDGED]</span> " if is_ack else ""

            st.markdown(
                f"""
                <div class="alert-box-{p.lower()}" style="opacity: {'0.6' if is_ack else '1.0'};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            {ack_tag}{badge_html} &nbsp; <b>{a['alert_title']}</b>
                        </div>
                        <span style="font-size:11px; color:#94a3b8;">{a['timestamp']}</span>
                    </div>
                    <div style="font-size:13px; color:#f8fafc; margin-top:6px;">
                        Aircraft: <b>{a['callsign']}</b> (<code>{a['icao24']}</code>) - {a['detected']}
                    </div>
                    <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">
                        <b>Trigger:</b> <code>{a['triggering_data']}</code> | <b>Action:</b> {a['suggested_verification']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_btn1, _ = st.columns([2, 6])
            with col_btn1:
                if is_ack:
                    if st.button("Unacknowledge", key=f"unack_{a['id']}"):
                        mgr.unacknowledge_alert(a["id"])
                        st.rerun()
                else:
                    if st.button("Mark Acknowledged", key=f"ack_{a['id']}"):
                        mgr.acknowledge_alert(a["id"])
                        st.rerun()
    else:
        st.info("No alerts match the selected criteria.")


# ============================================================
# NAVIGATION VIEW 7: ANALYTICS
# ============================================================

elif selected_nav == "7. Analytics":
    st.markdown("### 📈 Airspace Analytics & Fleet Distributions")
    st.caption("Visual analytics generated strictly from REAL received aircraft telemetry and weather data.")

    aircraft = st.session_state.aircraft_data
    alerts = st.session_state.active_alerts
    weather_reports = st.session_state.weather_data

    if not aircraft:
        st.warning("No real telemetry available yet. Please refresh data in the sidebar.")
    else:
        df = pd.DataFrame(aircraft)

        # Row 1: Altitude & Speed Distributions
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            fig_alt = plot_altitude_distribution(df)
            if fig_alt:
                st.plotly_chart(fig_alt, use_container_width=True)
            else:
                st.info("Altitude data unavailable.")

        with r1_c2:
            fig_spd = plot_speed_distribution(df)
            if fig_spd:
                st.plotly_chart(fig_spd, use_container_width=True)
            else:
                st.info("Velocity data unavailable.")

        # Row 2: Country Distribution & Airborne Ratio
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            fig_country = plot_country_distribution(df)
            if fig_country:
                st.plotly_chart(fig_country, use_container_width=True)
            else:
                st.info("Country data unavailable.")

        with r2_c2:
            fig_air = plot_airborne_ratio(df)
            if fig_air:
                st.plotly_chart(fig_air, use_container_width=True)
            else:
                st.info("Flight status data unavailable.")

        # Row 3: Vertical Profile & Alert Priority Breakdown
        r3_c1, r3_c2 = st.columns(2)
        with r3_c1:
            fig_vert = plot_vertical_flight_profile(df)
            if fig_vert:
                st.plotly_chart(fig_vert, use_container_width=True)
            else:
                st.info("Vertical rate profile unavailable.")

        with r3_c2:
            fig_alerts = plot_alert_priority_distribution(alerts)
            if fig_alerts:
                st.plotly_chart(fig_alerts, use_container_width=True)
            else:
                st.info("Zero active alerts currently to plot.")

        st.caption("Note: Based strictly on live received aircraft state vectors and weather reports. Historical multi-day dataset not yet available.")


# ============================================================
# NAVIGATION VIEW 8: AI ASSISTANT
# ============================================================

elif selected_nav == "8. AI Assistant":
    st.markdown("### 💬 Grounded AI Aviation Assistant")
    st.caption("Ask questions about the real aircraft, weather reports, and workload indicators currently monitored.")

    aircraft = st.session_state.aircraft_data
    alerts = st.session_state.active_alerts
    weather_reports = st.session_state.weather_data
    workload = st.session_state.workload_info

    # Sample prompt chips
    st.markdown("**Quick Inquiries:**")
    q1, q2, q3, q4 = st.columns(4)
    preset_query = None

    with q1:
        if st.button("✈️ What aircraft are monitored?", use_container_width=True):
            preset_query = "What aircraft are currently being monitored?"
    with q2:
        if st.button("🚨 Which aircraft require attention?", use_container_width=True):
            preset_query = "Which aircraft require attention?"
    with q3:
        if st.button("🔍 Explain highest priority alert", use_container_width=True):
            preset_query = "Explain the highest priority alert."
    with q4:
        if st.button("⚡ Why is workload elevated?", use_container_width=True):
            preset_query = "Why is the workload indicator elevated?"

    # Chat history display
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_prompt = st.chat_input("Ask about monitored flights, weather conditions, or alerts...")
    query_to_run = preset_query or user_prompt

    if query_to_run:
        # Append user message
        st.session_state.chat_messages.append({"role": "user", "content": query_to_run})
        with st.chat_message("user"):
            st.markdown(query_to_run)

        # Generate response grounded on real data
        with st.spinner("Analyzing live aviation data..."):
            ai_response = st.session_state.ai_agent.answer_query(
                query_to_run,
                aircraft,
                alerts,
                weather_reports,
                workload,
            )

        st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)


# ============================================================
# NAVIGATION VIEW 9: ABOUT
# ============================================================

elif selected_nav == "9. About":
    st.markdown("### ℹ️ About AeroGuardian AI")

    st.markdown(
        """
        <div class="aero-card-highlight">
            <h2 style="margin:0; color:#00e5ff;">AeroGuardian AI</h2>
            <p style="font-size:16px; color:#38bdf8; font-weight:600; margin-top:4px;">
                "An AI Agent for Pilot Workload & Decision Support"
            </p>
            <p style="font-size:14px; color:#94a3b8;">
                <b>Theme:</b> "Smart Systems for a Safer Future in Aviation"
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        #### 1. Core Mission & Purpose
        AeroGuardian AI is an intelligent aviation decision-support research prototype designed as a **Human-Factor Guardian**.
        In modern complex airspace, pilots and air traffic personnel face continuous multi-source data streams.
        AeroGuardian AI integrates real-time aircraft state vectors, terminal aerodrome weather, and transponder codes
        to prioritize attention-worthy flight conditions, explain operational significance, and calculate a transparent
        human-factor workload index.

        #### 2. Real Aviation Data Architecture
        Strictly real-world aviation feeds — no simulated, randomized, or fake values:
        - **OpenSky Network REST API**: Real-time Mode-S / ADS-B aircraft state vectors including ICAO24, callsign,
          position, barometric altitude, ground speed, true track, and squawk codes.
        - **NOAA Aviation Weather Center (AWC) Data API**: Live METAR and TAF observations, cloud layer bases,
          flight rules category (VFR, MVFR, IFR, LIFR), and convective clouds.
        - **Explainable Decision Engine**: Synthesizes risk rules, telemetry uncertainty, and contextual advice.
        - **AI Assistant**: Grounded question-answering powered by OpenAI API or internal semantic heuristics.

        #### 3. Technology Stack
        - **Language & Framework**: Python 3, Streamlit
        - **Data Handling**: Pandas, Requests, python-dotenv
        - **Visualizations**: Plotly Express & Plotly Graph Objects (Aerospace Dark Control-Room Theme)
        - **AI & Reasoning**: OpenAI API + Deterministic Aviation Heuristic Engine

        #### 4. Safety & Academic Research Limitations
        - **Research Prototype**: This software is created for academic research, education, and decision-support studies.
        - **Non-Operational**: Not certified by FAA, EASA, DGCA, or ICAO.
        - **Zero Control Authority**: AeroGuardian AI never commands aircraft maneuvers, manipulates autopilots,
          or overrides pilot-in-command / air traffic control authority.
        - **Cautious Terminology**: Always communicates uncertainty using standard scientific framing:
          *"Potential concern detected"*, *"Requires attention"*, *"Further verification recommended"*.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center; padding:15px; border-top:1px solid #1e293b; color:#64748b; font-size:12px;">
        <b>AeroGuardian AI</b> • Research & Educational Decision Support • 
        Real-Time Feeds from OpenSky Network & NOAA AWC • Not for operational flight control.
    </div>
    """,
    unsafe_allow_html=True,
)