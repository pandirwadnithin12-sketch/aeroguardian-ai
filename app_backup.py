import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AeroGuardian AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #0b1f3a;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 20px;
        color: #526174;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    /* Academic notice */
    .notice {
        background: #e8f2ff;
        border-left: 5px solid #1976d2;
        padding: 16px 20px;
        border-radius: 10px;
        color: #17324d;
        margin: 20px 0 30px 0;
    }

    /* Section title */
    .section-title {
        color: #0b1f3a;
        font-size: 26px;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #e3e8ef;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(20, 40, 70, 0.06);
    }

    .metric-label {
        color: #68778a;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        color: #0b1f3a;
        font-size: 30px;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-sub {
        color: #75859a;
        font-size: 13px;
        margin-top: 5px;
    }

    /* Information cards */
    .info-card {
        background: white;
        border: 1px solid #e3e8ef;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 3px 12px rgba(20, 40, 70, 0.05);
    }

    .info-label {
        color: #75859a;
        font-size: 13px;
        font-weight: 600;
    }

    .info-value {
        color: #172b4d;
        font-size: 18px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Risk card */
    .risk-card {
        background: white;
        border-radius: 14px;
        border: 1px solid #e3e8ef;
        padding: 22px;
        box-shadow: 0 3px 12px rgba(20, 40, 70, 0.06);
    }

    .risk-number {
        font-size: 42px;
        font-weight: 800;
        color: #d97706;
    }

    .risk-label {
        font-size: 14px;
        color: #68778a;
    }

    /* Alert card */
    .alert-card {
        background: #fff7ed;
        border-left: 6px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
    }

    .alert-title {
        font-size: 20px;
        font-weight: 750;
        color: #7c2d12;
    }

    .alert-text {
        color: #5b4636;
        margin-top: 8px;
    }

    /* Status badges */
    .badge-high {
        display: inline-block;
        background: #fee2e2;
        color: #991b1b;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
    }

    .badge-medium {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
    }

    .badge-low {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b1f3a;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #7a8797;
        font-size: 13px;
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #dce2e9;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "<h1 style='text-align:center;'>✈️</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align:center;'>AeroGuardian AI</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🤖 AI Guardian",
            "🎮 Scenario Simulator",
            "🔮 What-If Analysis",
            "🚨 Alert History",
            "📊 Analytics",
            "💬 AI Assistant",
            "ℹ️ About"
        ]
    )

    st.markdown("---")

    st.caption("Academic Prototype")
    st.caption("Simulated Aircraft Data")


# ============================================================
# SIMULATED AIRCRAFT DATA
# ============================================================

aircraft = {
    "Aircraft ID": "AG-204",
    "Flight Number": "AG-204",
    "Altitude": 35000,
    "Fuel": 64,
    "Engine Temperature": 92,
    "Engine Vibration": 78,
    "Cabin Pressure": 98,
    "Airspeed": 845,
    "Weather": "Moderate",
    "Destination": "Hyderabad"
}


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">✈️ AeroGuardian AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">An AI Agent for Pilot Workload & Decision Support</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="notice">
        🎓 <b>Academic Prototype</b> — This application uses simulated
        aircraft data and does not control real aircraft systems.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # FLIGHT STATUS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Flight Status</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">ALTITUDE</div>
            <div class="metric-value">35,000 ft</div>
            <div class="metric-sub">Cruising altitude</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">FUEL LEVEL</div>
            <div class="metric-value">64%</div>
            <div class="metric-sub">Fuel remaining</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">ENGINE TEMP</div>
            <div class="metric-value">92°C</div>
            <div class="metric-sub">Simulated reading</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">VIBRATION</div>
            <div class="metric-value">78%</div>
            <div class="metric-sub">Above normal range</div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # FLIGHT OVERVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🛫 Flight Overview</div>',
        unsafe_allow_html=True
    )

    o1, o2, o3, o4, o5 = st.columns(5)

    overview = [
        ("Aircraft ID", "AG-204"),
        ("Flight Number", "AG-204"),
        ("Flight Status", "IN FLIGHT"),
        ("Weather", "Moderate"),
        ("Destination", "Hyderabad")
    ]

    for column, (label, value) in zip(
        [o1, o2, o3, o4, o5],
        overview
    ):
        with column:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # AIRCRAFT SENSOR TABLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">✈️ Aircraft Sensor Status</div>',
        unsafe_allow_html=True
    )

    sensor_data = pd.DataFrame({
        "Parameter": [
            "Engine Temperature",
            "Engine Vibration",
            "Fuel Level",
            "Cabin Pressure",
            "Altitude",
            "Airspeed"
        ],
        "Value": [
            92,
            78,
            64,
            98,
            35000,
            845
        ],
        "Unit": [
            "°C",
            "%",
            "%",
            "%",
            "ft",
            "km/h"
        ],
        "Status": [
            "Normal",
            "Warning",
            "Normal",
            "Normal",
            "Normal",
            "Normal"
        ]
    })

    st.dataframe(
        sensor_data,
        width="stretch",
        hide_index=True
    )

    # --------------------------------------------------------
    # SENSOR CHART
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📈 Sensor Overview</div>',
        unsafe_allow_html=True
    )

    chart_data = pd.DataFrame({
        "Sensor": [
            "Engine Temp",
            "Vibration",
            "Fuel",
            "Cabin Pressure"
        ],
        "Value": [
            92,
            78,
            64,
            98
        ]
    })

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=chart_data["Sensor"],
            y=chart_data["Value"],
            text=chart_data["Value"],
            textposition="outside"
        )
    )

    fig.update_layout(
        title="Simulated Aircraft Sensor Values",
        yaxis_title="Value",
        xaxis_title="Sensor",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # --------------------------------------------------------
    # RISK ASSESSMENT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🎯 Overall Risk Assessment</div>',
        unsafe_allow_html=True
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        st.markdown("""
        <div class="risk-card">
            <div class="risk-label">SIMULATED RISK SCORE</div>
            <div class="risk-number">68/100</div>
            <span class="badge-medium">MEDIUM RISK</span>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown("""
        <div class="risk-card">
            <div class="risk-label">ACTIVE ALERTS</div>
            <div class="risk-number">1</div>
            <span class="badge-high">HIGH PRIORITY</span>
        </div>
        """, unsafe_allow_html=True)

    with r3:
        st.markdown("""
        <div class="risk-card">
            <div class="risk-label">SYSTEM STATUS</div>
            <div class="risk-number">OK</div>
            <span class="badge-low">MONITORING</span>
        </div>
        """, unsafe_allow_html=True)

    st.progress(0.68)

    # --------------------------------------------------------
    # AI PRIORITY ALERT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🚨 AI Priority Alert</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="alert-card">

        <div class="alert-title">
            ⚠️ High Engine Vibration Detected
        </div>

        <div class="alert-text">
            The simulated engine vibration value is currently 78%.
            AeroGuardian AI has classified this as a high-priority
            monitoring alert.
        </div>

        <br>

        <b>Severity:</b>
        <span class="badge-high">HIGH</span>

        &nbsp;&nbsp;

        <b>Status:</b>
        <span class="badge-medium">MONITORING</span>

        <br><br>

        <b>AI Decision Support:</b><br>
        Review the simulated engine condition and the relevant
        aircraft checklist. This recommendation is for academic
        simulation only.
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # RECENT AI DECISIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🧠 Recent AI Decisions</div>',
        unsafe_allow_html=True
    )

    decisions = pd.DataFrame({
        "Time": [
            "13:48:21",
            "13:47:05",
            "13:45:42"
        ],
        "Event": [
            "Engine vibration analyzed",
            "Fuel level checked",
            "Weather condition evaluated"
        ],
        "AI Result": [
            "High-priority monitoring",
            "Normal",
            "Moderate risk"
        ],
        "Status": [
            "⚠️ Warning",
            "✅ Normal",
            "⚠️ Monitor"
        ]
    })

    st.dataframe(
        decisions,
        width="stretch",
        hide_index=True
    )


# ============================================================
# AI GUARDIAN
# ============================================================

elif page == "🤖 AI Guardian":

    st.title("🤖 AI Guardian")

    st.info(
        "The AI Guardian analyzes simulated aircraft parameters "
        "and prioritizes potential risks."
    )

    temperature = aircraft["Engine Temperature"]
    vibration = aircraft["Engine Vibration"]
    fuel = aircraft["Fuel"]

    alerts = []

    if vibration >= 75:
        alerts.append(
            ("HIGH", "Engine vibration is elevated.")
        )

    if temperature >= 100:
        alerts.append(
            ("HIGH", "Engine temperature is elevated.")
        )

    if fuel <= 25:
        alerts.append(
            ("MEDIUM", "Fuel level is relatively low.")
        )

    if not alerts:
        alerts.append(
            ("LOW", "No major simulated risks detected.")
        )

    st.subheader("Risk Analysis")

    for severity, message in alerts:

        if severity == "HIGH":
            st.error(f"🔴 {severity} PRIORITY — {message}")

        elif severity == "MEDIUM":
            st.warning(f"🟡 {severity} PRIORITY — {message}")

        else:
            st.success(f"🟢 {severity} PRIORITY — {message}")

    st.subheader("AI Decision Support")

    st.write(
        """
        AeroGuardian AI combines the available simulated sensor
        information and prioritizes the most important event.

        Current priority:
        **Engine vibration monitoring**

        The system recommends reviewing the simulated engine
        condition and relevant checklist.
        """
    )


# ============================================================
# SCENARIO SIMULATOR
# ============================================================

elif page == "🎮 Scenario Simulator":

    st.title("🎮 Scenario Simulator")

    st.info(
        "Change simulated aircraft conditions and observe how "
        "the AI risk assessment changes."
    )

    col1, col2 = st.columns(2)

    with col1:

        sim_temperature = st.slider(
            "Engine Temperature (°C)",
            60,
            130,
            92
        )

        sim_vibration = st.slider(
            "Engine Vibration (%)",
            0,
            100,
            78
        )

        sim_fuel = st.slider(
            "Fuel Level (%)",
            0,
            100,
            64
        )

    with col2:

        sim_altitude = st.slider(
            "Altitude (ft)",
            5000,
            45000,
            35000,
            step=1000
        )

        sim_weather = st.slider(
            "Weather Severity",
            0,
            100,
            40
        )

        sim_pressure = st.slider(
            "Cabin Pressure (%)",
            80,
            100,
            98
        )

    if st.button("🚀 Run Simulation", type="primary"):

        risk = 0
        findings = []

        if sim_temperature > 100:
            risk += 25
            findings.append("High engine temperature")

        if sim_vibration > 75:
            risk += 30
            findings.append("High engine vibration")

        if sim_fuel < 30:
            risk += 20
            findings.append("Low fuel level")

        if sim_weather > 70:
            risk += 15
            findings.append("Severe weather")

        if sim_pressure < 90:
            risk += 20
            findings.append("Low cabin pressure")

        risk = min(risk, 100)

        st.divider()

        st.subheader("Simulation Result")

        st.metric(
            "Simulated Risk Score",
            f"{risk}/100"
        )

        if risk >= 70:
            st.error("🔴 HIGH RISK")

        elif risk >= 40:
            st.warning("🟡 MEDIUM RISK")

        else:
            st.success("🟢 LOW RISK")

        st.subheader("Detected Conditions")

        if findings:
            for item in findings:
                st.write(f"⚠️ {item}")
        else:
            st.success("No major simulated risks detected.")


# ============================================================
# WHAT-IF ANALYSIS
# ============================================================

elif page == "🔮 What-If Analysis":

    st.title("🔮 What-If Analysis")

    st.write(
        "Explore how individual simulated conditions can affect "
        "the overall risk score."
    )

    scenarios = {
        "Normal Flight": 20,
        "High Engine Vibration": 55,
        "High Engine Temperature": 60,
        "Low Fuel": 65,
        "Severe Weather": 70,
        "Multiple Alerts": 90
    }

    scenario_df = pd.DataFrame(
        list(scenarios.items()),
        columns=["Scenario", "Risk Score"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=scenario_df["Scenario"],
            y=scenario_df["Risk Score"],
            text=scenario_df["Risk Score"],
            textposition="outside"
        )
    )

    fig.update_layout(
        title="Simulated Risk Comparison",
        yaxis_title="Risk Score",
        xaxis_title="Scenario",
        yaxis=dict(range=[0, 100]),
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Example")

    st.write(
        """
        If engine vibration and severe weather occur at the same time,
        the AI Agent gives the combined situation a higher priority
        than either event individually.
        """
    )


# ============================================================
# ALERT HISTORY
# ============================================================

elif page == "🚨 Alert History":

    st.title("🚨 Alert History")

    history = pd.DataFrame({
        "Date": [
            "09-09-2026",
            "09-09-2026",
            "09-09-2026",
            "09-09-2026"
        ],
        "Time": [
            "13:48",
            "13:46",
            "13:44",
            "13:41"
        ],
        "Alert": [
            "Engine Vibration",
            "Weather Change",
            "Fuel Monitoring",
            "Engine Temperature"
        ],
        "Severity": [
            "HIGH",
            "MEDIUM",
            "LOW",
            "LOW"
        ],
        "Status": [
            "Monitoring",
            "Monitoring",
            "Normal",
            "Normal"
        ]
    })

    st.dataframe(
        history,
        width="stretch",
        hide_index=True
    )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.title("📊 Flight Analytics")

    st.subheader("Simulated Sensor Trends")

    trend_df = pd.DataFrame({
        "Time": [
            "13:40",
            "13:42",
            "13:44",
            "13:46",
            "13:48"
        ],
        "Engine Temperature": [
            86, 88, 89, 91, 92
        ],
        "Engine Vibration": [
            61, 65, 68, 73, 78
        ],
        "Fuel": [
            69, 68, 67, 65, 64
        ]
    })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=trend_df["Time"],
            y=trend_df["Engine Temperature"],
            mode="lines+markers",
            name="Engine Temperature"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend_df["Time"],
            y=trend_df["Engine Vibration"],
            mode="lines+markers",
            name="Engine Vibration"
        )
    )

    fig.update_layout(
        title="Engine Monitoring Trend",
        xaxis_title="Time",
        yaxis_title="Value",
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Alert Summary")

    a1, a2, a3 = st.columns(3)

    a1.metric("High Alerts", "1")
    a2.metric("Medium Alerts", "2")
    a3.metric("Low Alerts", "3")


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "💬 AI Assistant":

    st.title("💬 AeroGuardian AI Assistant")

    st.info(
        "Ask questions about the simulated flight data."
    )

    question = st.text_input(
        "Ask your question:"
    )

    if st.button("Ask AI"):

        if question.strip():

            q = question.lower()

            if "fuel" in q:
                answer = (
                    "The current simulated fuel level is 64%. "
                    "This is currently being monitored."
                )

            elif "vibration" in q:
                answer = (
                    "The simulated engine vibration is 78%, "
                    "which has been classified as a high-priority "
                    "monitoring alert."
                )

            elif "temperature" in q:
                answer = (
                    "The current simulated engine temperature is 92°C."
                )

            elif "risk" in q:
                answer = (
                    "The current simulated overall risk score is "
                    "68/100, classified as Medium Risk."
                )

            else:
                answer = (
                    "Based on the current simulated flight data, "
                    "the main priority is monitoring engine vibration."
                )

            st.success(answer)

        else:
            st.warning("Please enter a question.")


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About AeroGuardian AI")

    st.subheader("Project Overview")

    st.write(
        """
        AeroGuardian AI is an academic prototype designed to
        demonstrate how AI Agents can support pilot workload
        management and decision-making.

        The system analyzes simulated aircraft sensor information,
        identifies potential risks, prioritizes alerts, and provides
        explainable decision-support information.
        """
    )

    st.subheader("🎯 Problem Statement")

    st.write(
        """
        Modern aircraft generate large amounts of data and alerts.
        It can be difficult to quickly identify which information
        is most important.

        AeroGuardian AI addresses this challenge by organizing
        simulated information and prioritizing important events.
        """
    )

    st.subheader("🛠️ Technology Stack")

    tech = pd.DataFrame({
        "Technology": [
            "Python",
            "Streamlit",
            "Pandas",
            "Plotly",
            "OpenAI API",
            "SQLite"
        ],
        "Purpose": [
            "Programming",
            "Web Application",
            "Data Processing",
            "Data Visualization",
            "AI Agent",
            "Data Storage"
        ]
    })

    st.dataframe(
        tech,
        width="stretch",
        hide_index=True
    )

    st.warning(
        "⚠️ This is an academic simulation. "
        "It is not intended for real-world aircraft operation "
        "or flight control."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer">
        ✈️ AeroGuardian AI | Academic AI Agent Project<br>
        Simulated Data Only | Last Updated:
        {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
    </div>
    """,
    unsafe_allow_html=True
)