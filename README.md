# AeroGuardian AI 🛡️✈️
### "An AI Agent for Pilot Workload & Decision Support"
**Main Theme:** *"Smart Systems for a Safer Future in Aviation"*

---

## ⚖️ Safety & Academic Disclaimer
> **IMPORTANT:** AeroGuardian AI is a research and educational decision-support prototype. It is **not certified aviation software** and must **never** be used for aircraft flight control, operational flight clearance, or safety-critical air navigation.
> 
> The system **never** directly controls an aircraft, issues flight-control commands, or claims to replace licensed pilots or Air Traffic Control (ATC). All AI notifications use cautious scientific terminology:
> - *"Potential concern detected"*
> - *"Requires attention"*
> - *"Further verification recommended"*

---

## 📌 Project Overview
Modern pilots and air traffic personnel operate in data-dense environments, processing thousands of telemetry readings and meteorological variables concurrently. During non-nominal events, high information volume can cause cognitive saturation and information overload.

**AeroGuardian AI** acts as a **Human-Factor Guardian**, continuously analyzing:
- **Real-time aircraft state vectors** from OpenSky Network (positions, barometric/geometric altitudes, ground speeds, true tracks, vertical rates, transponder squawk codes)
- **Real aviation weather** from NOAA Aviation Weather Center (METAR, TAF, flight category VFR/MVFR/IFR/LIFR, wind vectors, gusts, visibility, cloud ceilings, convective clouds)
- **Multi-source situational complexity**

Instead of displaying uncurated raw streams, the AI Agent prioritizes attention-worthy conditions, reduces information overload, and provides explainable reasoning for each observation.

---

## 🚀 Architecture: React Frontend + Python REST API

The application is built with a modern, responsive **React 18 Single Page Application** frontend and a high-performance **Starlette + Uvicorn ASGI REST API** backend, preserving all real-data ML, risk, and weather models.

```
                    ┌──────────────────────────────────────────────┐
                    │       REACT 18 SINGLE PAGE APPLICATION       │
                    │                                              │
                    │   • Lucide Icons (Shield, Plane, Radio, etc) │
                    │   • Interactive Leaflet Radar Map            │
                    │   • True-heading rotated SVG aircraft pins   │
                    │   • Pulse beacons for priority alerts        │
                    │   • 9 Integrated Navigation Views            │
                    │   • Real-time auto-refresh & countdown       │
                    │   • Web Audio API avionics caution chime     │
                    │   • Radar HUD sweep animation toggle         │
                    │   • One-click telemetry CSV export           │
                    └──────────────────────┬───────────────────────┘
                                           │ JSON REST API
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │      STARLETTE ASGI SERVER (server.py)       │
                    │             Uvicorn on Port 8000             │
                    └──────┬──────────────┬──────────────┬─────────┘
                           │              │              │
                           ▼              ▼              ▼
                    ┌──────────────┐┌──────────────┐┌──────────────┐
                    │opensky_client││weather_client││ risk_engine  │
                    │Real ADS-B/M-S││NOAA METAR/TAF││Anomaly Rules │
                    └──────┬───────┘└──────┬───────┘└──────┬───────┘
                           │               │               │
                           └───────┬───────┴───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      ai_agent.py             │
                    │ Workload Index (0-100%)      │
                    │ Situation Awareness Summary  │
                    │ Grounded AI Assistant        │
                    └──────────────────────────────┘
```

---

## 🧭 9 Main Views & Features

1. **Mission Dashboard**: Top 5 KPI cards, live radar map, AI situation awareness summary, priority alerts stream with acknowledge toggles, and live terminal weather cards.
2. **Live Aircraft**: Interactive radar map, fuzzy instant search, status filter (Airborne/Ground/Attention), sortable telemetry table, CSV export, and Aircraft Diagnostic Drawer with Mode-S completeness audit.
3. **Aviation Weather**: Station selector with presets (`VIDP`, `VOBL`, `VABB`, `VOHS`, `OMDB`, `EGLL`, `KJFK`, etc.) and custom ICAO search; decoded METAR, flight category badge (`VFR`/`MVFR`/`IFR`/`LIFR`), wind vector, visibility, temperature/dewpoint spread, cloud ceiling with CB detection, and TAF forecast timeline.
4. **AI Guardian**: Executive situation report and structured risk detection cards with explainable reasoning (*What was detected*, *Why it matters*, *Triggering data*, *Confidence*, *Suggested verification*).
5. **Workload Analysis**: Interactive SVG gauge for the "AI-Assisted Workload Indicator — Research Prototype", multi-factor radar breakdown, contributing factor table with weights, and human factors research notes.
6. **Alert Center**: Full alert triage board, priority filters (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), operator acknowledgment tracking, and clear acknowledged button.
7. **Analytics**: Real data distribution charts for barometric altitude (FL), ground speed (kts), top countries of registration, airborne ratio, and vertical flight profiles.
8. **AI Assistant**: Interactive conversational terminal grounded in live telemetry and weather data, with quick inquiry prompt chips.
9. **About**: Research mission, theme, data sources, architecture, and academic safety disclaimers.

---

## 📂 Project Structure

```
aero guardian AI/
├── static/                 # React 18 Frontend
│   ├── index.html          # HTML5 SPA shell (loads React, Leaflet, Lucide)
│   ├── index.css           # Modern aerospace glassmorphism design system
│   └── app.jsx             # React master app (Lucide icons, Leaflet radar, 9 views)
├── server.py               # Starlette ASGI REST API server & static asset host
├── run.py                  # Single-command launcher (starts server & opens browser)
├── opensky_client.py       # OpenSky Network live aircraft client with caching
├── weather_client.py       # NOAA Aviation Weather Center METAR & TAF client
├── risk_engine.py          # Real telemetry anomaly & risk detection rules
├── alert_manager.py        # Alert prioritization, deduplication, and acknowledgment
├── ai_agent.py             # AI Guardian Agent, workload model, and grounded assistant
├── analytics.py            # Analytics helpers & aggregations
├── utils.py                # Aviation unit conversions and formatters
├── requirements.txt        # Python dependency specifications
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules for credentials and cache
└── README.md               # Project documentation and research disclaimers
```

---

## 🚀 Running the Application

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Launch the Application
Run the single-command launcher:
```powershell
python run.py
```
Or start the server directly:
```powershell
python server.py
```

Open your browser at:
```
http://localhost:8000
```

---

## 🌐 Live Production Deployment
AeroGuardian AI is deployed on Vercel:
- **Production URL:** [https://aeroguardian-ai.vercel.app](https://aeroguardian-ai.vercel.app)
- **API Status:** [https://aeroguardian-ai.vercel.app/api/status](https://aeroguardian-ai.vercel.app/api/status)
- **Consolidated Master Telemetry:** [https://aeroguardian-ai.vercel.app/api/all](https://aeroguardian-ai.vercel.app/api/all)

