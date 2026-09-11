"""
AeroGuardian AI - High-Performance REST API Server (Starlette + Uvicorn)

Exposes real-time aviation endpoints wrapping existing models:
- OpenSky Network client
- NOAA Aviation Weather Center client
- Risk Engine
- Alert Manager
- AI Guardian Agent (Workload & Situation Awareness)
- Analytics & Unit Converters

Serves the React Single Page Application on http://localhost:8000
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import existing backend models (unmodified)
from opensky_client import (
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
from utils import (
    meters_to_feet,
    ms_to_knots,
    ms_to_kmh,
    ms_to_ft_per_min,
    km_to_nm,
    hpa_to_inhg,
    fmt_val,
    fmt_altitude,
    fmt_speed,
    fmt_vertical_rate,
    fmt_heading,
    fmt_squawk,
    estimate_mach,
    classify_flight_phase,
    get_wake_category,
    calculate_bearing,
    calculate_wind_components,
)
from risk_engine import calculate_distance_approx
from flight_routes import resolve_flight_route, AIRPORTS_DB

load_dotenv()

# Global state instances
alert_mgr = AlertManager()
ai_agent = AIGuardianAgent()

_STATE: Dict[str, Any] = {
    "monitored_region": "India",
    "aircraft": [],
    "weather": [],
    "alerts": [],
    "workload": {},
    "situation": {},
    "last_refresh": 0.0,
    "last_refresh_str": None,
}


def refresh_data(force: bool = False) -> Dict[str, Any]:
    """Execute real data pipeline and update application cache."""
    now = time.time()
    # Respect rate limiting unless forcing refresh
    if not force and _STATE["aircraft"] and (now - _STATE["last_refresh"]) < 12.0:
        return _STATE

    region = _STATE["monitored_region"]

    # 1. Fetch real aircraft
    try:
        aircraft = get_live_aircraft_by_region(region, force_refresh=force)
        _STATE["aircraft"] = aircraft
    except Exception as e:
        aircraft = _STATE["aircraft"]

    # 2. Fetch real weather
    try:
        weather = get_weather_overview(["VIDP", "VOBL", "VABB", "VOHS", "VECC", "VOMM"])
        _STATE["weather"] = weather
    except Exception as e:
        weather = _STATE["weather"]

    # 3. Enrich aircraft records with end-to-end aeroplane telemetry
    enriched_aircraft = []
    for p in aircraft:
        plane = dict(p)
        v_ms = plane.get("velocity")
        alt_m = plane.get("baro_altitude")
        vr_ms = plane.get("vertical_rate")
        lat = plane.get("latitude")
        lon = plane.get("longitude")
        hdg = plane.get("heading")
        last_c = plane.get("time_position") or plane.get("last_contact")

        # Altitude conversions & Flight Level
        alt_ft = meters_to_feet(alt_m) if alt_m is not None else None
        plane["altitude_ft"] = round(alt_ft) if alt_ft is not None else None
        if alt_ft is not None:
            plane["flight_level"] = f"FL{int(round(alt_ft/100))}" if alt_ft >= 10000 else f"{int(round(alt_ft)):,} ft"
        else:
            plane["flight_level"] = "N/A"

        # Speed conversions & Mach
        spd_kts = ms_to_knots(v_ms) if v_ms is not None else None
        plane["speed_kts"] = round(spd_kts) if spd_kts is not None else None
        plane["speed_kmh"] = round(ms_to_kmh(v_ms)) if v_ms is not None else None
        plane["mach"] = estimate_mach(v_ms, alt_m)

        # Vertical rate & VSI
        vr_fpm = ms_to_ft_per_min(vr_ms) if vr_ms is not None else None
        plane["vertical_rate_fpm"] = round(vr_fpm) if vr_fpm is not None else None

        # Flight Phase Classification
        plane["flight_phase"] = classify_flight_phase(plane)

        # Wake Turbulence Category
        plane["wake_category"] = get_wake_category(plane.get("category"))

        # Telemetry Freshness
        plane["telemetry_age"] = max(0, int(now - last_c)) if last_c is not None else None

        # Nearest Aerodrome Calculation & Wind Vector
        nearest_apt = None
        if lat is not None and lon is not None and weather:
            min_dist = float("inf")
            best_w = None
            for w in weather:
                w_lat = w.get("latitude")
                w_lon = w.get("longitude")
                if w_lat is not None and w_lon is not None:
                    dist_km = calculate_distance_approx(lat, lon, w_lat, w_lon)
                    if dist_km < min_dist:
                        min_dist = dist_km
                        best_w = w

            if best_w:
                dist_nm = km_to_nm(min_dist)
                bearing = calculate_bearing(lat, lon, best_w["latitude"], best_w["longitude"])
                wind_comp = calculate_wind_components(hdg, best_w.get("wind_dir_deg"), best_w.get("wind_speed_kt"))
                nearest_apt = {
                    "icao": best_w.get("icao"),
                    "name": best_w.get("name"),
                    "latitude": best_w.get("latitude"),
                    "longitude": best_w.get("longitude"),
                    "distance_nm": round(dist_nm, 1),
                    "distance_km": round(min_dist, 1),
                    "bearing_deg": bearing,
                    "flight_category": best_w.get("flight_category", "VFR"),
                    "wind_speed_kt": best_w.get("wind_speed_kt"),
                    "wind_dir_deg": best_w.get("wind_dir_deg"),
                    "crosswind_kt": wind_comp.get("crosswind_kt"),
                    "crosswind_dir": wind_comp.get("crosswind_dir"),
                    "headwind_kt": wind_comp.get("headwind_kt"),
                    "is_tailwind": wind_comp.get("is_tailwind"),
                }
        plane["nearest_airport"] = nearest_apt
        plane["route"] = resolve_flight_route(plane)
        enriched_aircraft.append(plane)

    aircraft = enriched_aircraft
    _STATE["aircraft"] = aircraft

    # 4. Evaluate real risks
    raw_alerts = evaluate_airspace_risks(aircraft, weather)

    # 5. Sync alert manager
    _STATE["alerts"] = alert_mgr.sync_alerts(raw_alerts)

    # 6. Calculate workload & situation awareness
    _STATE["workload"] = ai_agent.calculate_workload_indicator(
        aircraft, _STATE["alerts"], weather
    )
    _STATE["situation"] = ai_agent.generate_situation_summary(
        aircraft, _STATE["alerts"], weather
    )

    _STATE["last_refresh"] = now
    _STATE["last_refresh_str"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    return _STATE


# ============================================================
# REST API HANDLERS
# ============================================================

def get_map_config_data():
    load_dotenv(override=True)
    mapbox_token = os.getenv("MAPBOX_ACCESS_TOKEN") or os.getenv("MAPBOX_API_KEY") or ""
    maptiler_key = os.getenv("MAPTILER_API_KEY") or ""
    general_key = os.getenv("MAP_API_KEY") or ""
    active_key = mapbox_token or general_key or maptiler_key or ""
    provider = "mapbox" if mapbox_token else ("maptiler" if maptiler_key else ("custom" if general_key else "free_open_basemap"))
    return {
        "mapbox_token": mapbox_token,
        "maptiler_key": maptiler_key,
        "map_api_key": general_key,
        "active_key": active_key,
        "provider": provider,
        "has_api_key": bool(active_key),
    }


async def api_status(request):
    """Return external data feed connectivity status."""
    sky_status = get_opensky_status()
    wx_status = get_weather_status()
    return JSONResponse(
        {
            "opensky": sky_status,
            "weather": wx_status,
            "ai_engine": {
                "active": True,
                "provider": "OpenAI" if ai_agent.client else "Deterministic Heuristics",
                "model": ai_agent.model_name if ai_agent.client else "AeroGuardian-V2",
            },
            "map": get_map_config_data(),
            "region": _STATE["monitored_region"],
            "last_refresh": _STATE["last_refresh_str"],
        }
    )


async def api_map_config_get(request):
    """Return map configuration and API keys from environment."""
    return JSONResponse(get_map_config_data())


async def api_map_config_post(request):
    """Save map API key into environment and .env file."""
    try:
        body = await request.json()
        key = body.get("api_key", "").strip()
        provider = body.get("provider", "mapbox").strip().lower()

        if provider == "maptiler":
            os.environ["MAPTILER_API_KEY"] = key
        elif provider == "custom":
            os.environ["MAP_API_KEY"] = key
        else:
            os.environ["MAPBOX_ACCESS_TOKEN"] = key
            os.environ["MAP_API_KEY"] = key

        env_path = os.path.join(os.path.dirname(__file__), ".env")
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        target_var = "MAPBOX_ACCESS_TOKEN" if provider == "mapbox" else ("MAPTILER_API_KEY" if provider == "maptiler" else "MAP_API_KEY")
        key_written = False
        new_lines = []
        for l in lines:
            if l.startswith("MAPBOX_ACCESS_TOKEN=") and target_var == "MAPBOX_ACCESS_TOKEN":
                new_lines.append(f"MAPBOX_ACCESS_TOKEN={key}\n")
                key_written = True
            elif l.startswith("MAPTILER_API_KEY=") and target_var == "MAPTILER_API_KEY":
                new_lines.append(f"MAPTILER_API_KEY={key}\n")
                key_written = True
            elif l.startswith("MAP_API_KEY=") and target_var == "MAP_API_KEY":
                new_lines.append(f"MAP_API_KEY={key}\n")
                key_written = True
            else:
                new_lines.append(l)

        if not key_written:
            new_lines.append(f"{target_var}={key}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        return JSONResponse({"status": "success", "api_key": key, "provider": provider, "has_api_key": bool(key)})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


async def api_aircraft(request):
    """Return live aircraft state vectors for current region."""
    region = request.query_params.get("region")
    force = request.query_params.get("refresh", "false").lower() == "true"

    if region and region in REGION_BOUNDS and region != _STATE["monitored_region"]:
        _STATE["monitored_region"] = region
        force = True

    data = refresh_data(force=force)
    return JSONResponse(
        {
            "count": len(data["aircraft"]),
            "region": _STATE["monitored_region"],
            "last_refresh": _STATE["last_refresh_str"],
            "aircraft": data["aircraft"],
        }
    )


async def api_aircraft_diagnostic(request):
    """Return deep AI explainable diagnostic for a specific aircraft."""
    icao24 = request.path_params["icao24"]
    aircraft_list = _STATE["aircraft"]
    plane = next((p for p in aircraft_list if p.get("icao24") == icao24), None)

    if not plane:
        return JSONResponse({"error": f"Aircraft {icao24} not found in monitored state"}, status_code=404)

    diag = ai_agent.analyze_aircraft_detail(plane, _STATE["alerts"], _STATE["weather"])

def get_contextual_checklist(phase_code: str, observations: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Build dynamic decision-support checklist based on flight phase & alerts."""
    checklist = []
    if phase_code == "GROUND":
        checklist.extend([
            {"id": "c1", "item": "Verify ATC taxi route clearance and assigned departure runway", "done": False},
            {"id": "c2", "item": "Confirm transponder set to assigned departure squawk code", "done": False},
            {"id": "c3", "item": "Review departure aerodrome ATIS / METAR and altimeter setting (QNH)", "done": False},
            {"id": "c4", "item": "Cross-check departure runway surface condition and crosswind limits", "done": False},
        ])
    elif phase_code in ("TAKEOFF", "CLIMB"):
        checklist.extend([
            {"id": "c1", "item": "Monitor initial climb speed and pitch limit margins", "done": False},
            {"id": "c2", "item": "Verify transition altitude altimeter setting (Standard 1013.2 hPa / 29.92 inHg)", "done": False},
            {"id": "c3", "item": "Confirm climb clearance to en-route cruise flight level", "done": False},
            {"id": "c4", "item": "Check engine climb thrust rating and airspeed acceleration", "done": False},
        ])
    elif phase_code == "CRUISE":
        checklist.extend([
            {"id": "c1", "item": "Cross-check cruise Mach number and aerodynamic buffet margin", "done": False},
            {"id": "c2", "item": "Compare actual fuel burn versus flight plan scheduled burn rate", "done": False},
            {"id": "c3", "item": "Review high-altitude jet stream and CAT (Clear Air Turbulence) SIGMETs", "done": False},
            {"id": "c4", "item": "Identify nearest suitable en-route diversion aerodromes & runway lengths", "done": False},
        ])
    elif phase_code == "DESCENT":
        checklist.extend([
            {"id": "c1", "item": "Obtain latest destination aerodrome ATIS / METAR report", "done": False},
            {"id": "c2", "item": "Verify 250 kts speed restriction compliance below 10,000 ft MSL", "done": False},
            {"id": "c3", "item": "Cross-check top-of-descent vertical profile and speed brake deployment", "done": False},
            {"id": "c4", "item": "Brief descent arrival routing and Minimum Safe Altitude (MSA)", "done": False},
        ])
    elif phase_code == "APPROACH":
        checklist.extend([
            {"id": "c1", "item": "Confirm stabilized approach criteria met before 1,000 ft AGL", "done": False},
            {"id": "c2", "item": "Verify runway surface wind and calculated crosswind component", "done": False},
            {"id": "c3", "item": "Confirm missed approach / go-around altitude and missed approach procedure briefed", "done": False},
            {"id": "c4", "item": "Check landing gear down-and-locked and flap configuration", "done": False},
        ])
    else:
        checklist.extend([
            {"id": "c1", "item": "Verify assigned flight level and heading vector adherence", "done": False},
            {"id": "c2", "item": "Monitor airspeed margin and fuel remaining", "done": False},
            {"id": "c3", "item": "Maintain continuous watch on transponder squawk code", "done": False},
        ])

    if observations:
        alert_idx = 100
        for a in observations:
            if a.get("priority") in ("CRITICAL", "HIGH"):
                checklist.insert(0, {
                    "id": f"alert_chk_{alert_idx}",
                    "item": f"⚠️ URGENT ACTION: {a.get('suggested_action')}",
                    "done": False,
                    "urgent": True,
                })
                alert_idx += 1

    return checklist


async def api_aircraft_diagnostic(request):
    """Return deep AI explainable diagnostic for a specific aircraft."""
    icao24 = request.path_params["icao24"]
    aircraft_list = _STATE["aircraft"]
    plane = next((p for p in aircraft_list if p.get("icao24") == icao24), None)

    if not plane:
        return JSONResponse({"error": f"Aircraft {icao24} not found in monitored state"}, status_code=404)

    diag = ai_agent.analyze_aircraft_detail(plane, _STATE["alerts"], _STATE["weather"])

    phase_code = plane.get("flight_phase", {}).get("code", "LEVEL")
    diag["checklist"] = get_contextual_checklist(phase_code, diag.get("observations"))
    diag["flight_phase"] = plane.get("flight_phase")
    diag["mach"] = plane.get("mach")
    diag["flight_level"] = plane.get("flight_level")
    diag["speed_kts"] = plane.get("speed_kts")
    diag["speed_kmh"] = plane.get("speed_kmh")
    diag["altitude_ft"] = plane.get("altitude_ft")
    diag["vertical_rate_fpm"] = plane.get("vertical_rate_fpm")
    diag["wake_category"] = plane.get("wake_category")
    diag["nearest_airport"] = plane.get("nearest_airport")
    diag["telemetry_age"] = plane.get("telemetry_age")

    return JSONResponse(diag)


async def api_weather_overview(request):
    """Return monitored weather stations."""
    data = refresh_data()
    return JSONResponse({"stations": data["weather"]})


async def api_weather_station(request):
    """Return decoded METAR & TAF for any ICAO station code."""
    icao = request.path_params["icao"].strip().upper()
    metar = get_metar(icao)
    taf = get_taf(icao)

    if not metar:
        return JSONResponse({"error": f"Station {icao} unavailable in NOAA database"}, status_code=404)

    return JSONResponse({"metar": metar, "taf": taf})


async def api_alerts(request):
    """Return prioritized alerts with filter options."""
    pri = request.query_params.get("priority", "ALL")
    inc_ack = request.query_params.get("include_acknowledged", "true").lower() == "true"
    query = request.query_params.get("query")

    active_alerts = alert_mgr.get_active_alerts(
        priority_filter=pri if pri != "ALL" else None,
        include_acknowledged=inc_ack,
        search_query=query,
    )
    counts = alert_mgr.get_severity_counts()

    return JSONResponse(
        {
            "alerts": active_alerts,
            "counts": counts,
            "total_active": len(active_alerts),
        }
    )


async def api_alert_acknowledge(request):
    """Acknowledge an alert."""
    alert_id = request.path_params["alert_id"]
    success = alert_mgr.acknowledge_alert(alert_id)
    return JSONResponse({"success": success, "alert_id": alert_id})


async def api_alert_unacknowledge(request):
    """Unacknowledge an alert."""
    alert_id = request.path_params["alert_id"]
    success = alert_mgr.unacknowledge_alert(alert_id)
    return JSONResponse({"success": success, "alert_id": alert_id})


async def api_alert_clear_acknowledged(request):
    """Clear acknowledged alerts."""
    alert_mgr.clear_acknowledged()
    return JSONResponse({"success": True})


async def api_workload(request):
    """Return calculated research workload indicator and factor breakdown."""
    data = refresh_data()
    return JSONResponse(data["workload"])


async def api_situation(request):
    """Return AI situation awareness summary."""
    data = refresh_data()
    return JSONResponse(data["situation"])


async def api_assistant(request):
    """Conversational aviation assistant grounded in live telemetry and weather."""
    try:
        body = await request.json()
        query = body.get("query", "").strip()
    except Exception:
        query = ""

    if not query:
        return JSONResponse({"error": "Query required"}, status_code=400)

    data = refresh_data()
    response_text = ai_agent.answer_query(
        query,
        data["aircraft"],
        data["alerts"],
        data["weather"],
        data["workload"],
    )
    return JSONResponse({"query": query, "response": response_text})


async def api_analytics(request):
    """Return aggregated statistical distributions of current real data."""
    data = refresh_data()
    aircraft = data["aircraft"]
    alerts = data["alerts"]

    if not aircraft:
        return JSONResponse({"error": "No telemetry available"}, status_code=503)

    altitudes = [
        int(meters_to_feet(p["baro_altitude"]))
        for p in aircraft
        if p.get("baro_altitude") is not None
    ]
    speeds = [
        int(ms_to_knots(p["velocity"]))
        for p in aircraft
        if p.get("velocity") is not None
    ]

    countries: Dict[str, int] = {}
    for p in aircraft:
        c = p.get("country") or "Unknown"
        countries[c] = countries.get(c, 0) + 1

    top_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]

    airborne = sum(1 for p in aircraft if not p.get("on_ground", False))
    ground = len(aircraft) - airborne

    v_rates = [
        ms_to_ft_per_min(p["vertical_rate"])
        for p in aircraft
        if p.get("vertical_rate") is not None and not p.get("on_ground", False)
    ]
    climbing = sum(1 for r in v_rates if r > 300)
    descending = sum(1 for r in v_rates if r < -300)
    level = len(v_rates) - climbing - descending

    alert_counts = alert_mgr.get_severity_counts()

    return JSONResponse(
        {
            "total_aircraft": len(aircraft),
            "airborne": airborne,
            "ground": ground,
            "altitudes": altitudes,
            "speeds": speeds,
            "top_countries": [{"country": c[0], "count": c[1]} for c in top_countries],
            "vertical_profile": {
                "climbing": climbing,
                "level": level,
                "descending": descending,
            },
            "alert_distribution": alert_counts,
        }
    )


async def api_all(request):
    """
    Consolidated Single-URL Master Endpoint.
    Returns all real-time operational details in one URL:
    - System status & connectivity
    - AI Situation Awareness & Workload Index
    - Full Fleet Telemetry with Lifecycle Phases, Mach, and Nearest Aerodromes
    - Active Safety Alerts & Triage Counts
    - Terminal Aerodrome Weather (NOAA METARs)
    - Operational Analytics
    """
    region = request.query_params.get("region")
    force = request.query_params.get("refresh", "false").lower() == "true"

    if region and region in REGION_BOUNDS and region != _STATE["monitored_region"]:
        _STATE["monitored_region"] = region
        force = True

    data = refresh_data(force=force)
    sky_status = get_opensky_status()
    wx_status = get_weather_status()
    alert_counts = alert_mgr.get_severity_counts()

    enriched_aircraft_with_checklists = []
    for p in data["aircraft"]:
        p_copy = dict(p)
        phase_info = p.get("flight_phase")
        phase_code = phase_info.get("code", "LEVEL") if isinstance(phase_info, dict) else "LEVEL"
        chkl = get_contextual_checklist(phase_code)
        p_copy["checklist"] = chkl
        p_copy["decision_support_checklist"] = chkl
        enriched_aircraft_with_checklists.append(p_copy)

    v_rates = [p.get("vertical_rate_fpm") or 0 for p in data["aircraft"]]
    climbing = sum(1 for r in v_rates if r > 300)
    descending = sum(1 for r in v_rates if r < -300)
    level = len(v_rates) - climbing - descending

    return JSONResponse(
        {
            "meta": {
                "system": "AeroGuardian AI",
                "tagline": "An AI Agent for Pilot Workload & Decision Support",
                "theme": "Smart Systems for a Safer Future in Aviation",
                "monitored_region": _STATE["monitored_region"],
                "last_refresh_utc": _STATE["last_refresh_str"],
                "data_source_mode": sky_status.get("status_text"),
                "documentation": "Consolidated Master API - All real-time telemetry, avionics, weather, and checklists in one response.",
            },
            "status": {
                "opensky_adsb": sky_status,
                "noaa_weather": wx_status,
                "ai_guardian_engine": {
                    "active": True,
                    "model": ai_agent.model_name if ai_agent.client else "AeroGuardian-V2",
                },
            },
            "situation_awareness": _STATE["situation"],
            "workload_indicator": _STATE["workload"],
            "alert_summary": {
                "total_alerts": len(_STATE["alerts"]),
                "severity_counts": alert_counts,
                "active_alerts": _STATE["alerts"],
            },
            "terminal_weather": {
                "station_count": len(_STATE["weather"]),
                "stations": _STATE["weather"],
            },
            "flight_fleet": {
                "total_aircraft": len(data["aircraft"]),
                "airborne_count": sum(1 for p in data["aircraft"] if not p.get("on_ground")),
                "ground_count": sum(1 for p in data["aircraft"] if p.get("on_ground")),
                "aircraft": enriched_aircraft_with_checklists,
            },
            "analytics_summary": {
                "vertical_profile": {
                    "climbing": climbing,
                    "level": level,
                    "descending": descending,
                },
            },
        }
    )


async def api_airports(request):
    return JSONResponse(AIRPORTS_DB)


# Serve index.html for root
async def serve_index(request):
    root_index = os.path.join(os.path.dirname(__file__), "index.html")
    static_index = os.path.join(os.path.dirname(__file__), "static", "index.html")
    index_file = root_index if os.path.exists(root_index) else static_index
    if os.path.exists(index_file):
        response = FileResponse(index_file)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return JSONResponse({"message": "AeroGuardian AI API active. Build static assets."})


# ============================================================
# STARLETTE APPLICATION SETUP
# ============================================================

base_api_routes = [
    ("/all", api_all, ["GET"]),
    ("/master", api_all, ["GET"]),
    ("/status", api_status, ["GET"]),
    ("/aircraft", api_aircraft, ["GET"]),
    ("/aircraft/{icao24}/diagnostic", api_aircraft_diagnostic, ["GET"]),
    ("/weather/overview", api_weather_overview, ["GET"]),
    ("/weather/station/{icao}", api_weather_station, ["GET"]),
    ("/alerts", api_alerts, ["GET"]),
    ("/alerts/{alert_id}/acknowledge", api_alert_acknowledge, ["POST"]),
    ("/alerts/{alert_id}/unacknowledge", api_alert_unacknowledge, ["POST"]),
    ("/alerts/clear-acknowledged", api_alert_clear_acknowledged, ["POST"]),
    ("/workload", api_workload, ["GET"]),
    ("/situation", api_situation, ["GET"]),
    ("/assistant", api_assistant, ["POST"]),
    ("/analytics", api_analytics, ["GET"]),
    ("/config/map", api_map_config_get, ["GET"]),
    ("/config/map", api_map_config_post, ["POST"]),
    ("/airports", api_airports, ["GET"]),
]

routes = []
for suffix, handler, methods in base_api_routes:
    routes.append(Route(f"/api{suffix}", handler, methods=methods))
    routes.append(Route(suffix, handler, methods=methods))

routes.append(Route("/api", api_status, methods=["GET"]))
routes.append(Route("/api/index.py", api_status, methods=["GET"]))
routes.append(Route("/", serve_index, methods=["GET"]))

# Ensure static directory exists
static_path = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_path, exist_ok=True)
routes.append(Mount("/static", StaticFiles(directory=static_path), name="static"))

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = Starlette(debug=False, routes=routes, middleware=middleware)


if __name__ == "__main__":
    print("==================================================")
    print("[AEROGUARDIAN AI] REST API & REACT SERVER")
    print(">> Starting server on http://localhost:8000")
    print("==================================================")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
