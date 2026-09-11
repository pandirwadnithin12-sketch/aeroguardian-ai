"""
AeroGuardian AI - AI Guardian Agent & Human-Factor Workload Engine

Synthesizes real-time aircraft telemetry, weather observations, and risk events.
Provides:
1. AI Situation Awareness Summaries
2. AI-Assisted Workload Indicator (Research Prototype)
3. Explainable Reasoning & Attention Recommendations
4. Real Context-Grounded AI Assistant (OpenAI API + Intelligent Fallback)

Strict adherence to academic constraints: Never claims clinical validation or flight-control authority.
"""

import os
import math
import re
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv

from utils import (
    meters_to_feet,
    ms_to_knots,
    ms_to_kmh,
    ms_to_ft_per_min,
    calculate_distance_approx,
    calculate_bearing,
    calculate_wind_components,
    estimate_mach,
    classify_flight_phase,
    get_wake_category,
    km_to_nm,
)

load_dotenv()

# Check for OpenAI availability
OPENAI_AVAILABLE = False
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIGuardianAgent:
    """Intelligent Aviation Human-Factor Guardian and Decision Support Agent."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._init_openai()

    def _init_openai(self):
        """Initialize OpenAI client if API key is present."""
        self.client = None
        if OPENAI_AVAILABLE and self.api_key and "your_" not in self.api_key.lower():
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None

    def set_api_key(self, key: str):
        """Allow dynamic API key configuration from UI."""
        self.api_key = key
        self._init_openai()

    # ============================================================
    # 1. HUMAN FACTOR / WORKLOAD ANALYSIS (Research Prototype)
    # ============================================================

    def calculate_workload_indicator(
        self,
        aircraft_list: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        weather_reports: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculates a transparent multi-factor RESEARCH PROTOTYPE workload indicator.
        Based strictly on observable environment complexity:
        1. Alert Volume & Criticality (40% weight)
        2. Dynamic State Complexity (25% weight)
        3. Weather & Convective Complexity (20% weight)
        4. Telemetry Gap / Uncertainty Factor (15% weight)
        """
        total_aircraft = len(aircraft_list)
        airborne_aircraft = [p for p in aircraft_list if not p.get("on_ground", False)]
        airborne_count = len(airborne_aircraft)

        # Factor 1: Alert Severity Load (0 to 100)
        critical_count = sum(1 for a in alerts if a.get("priority") == "CRITICAL")
        high_count = sum(1 for a in alerts if a.get("priority") == "HIGH")
        medium_count = sum(1 for a in alerts if a.get("priority") == "MEDIUM")
        low_count = sum(1 for a in alerts if a.get("priority") == "LOW")

        alert_raw = (critical_count * 40) + (high_count * 20) + (medium_count * 10) + (low_count * 3)
        alert_score = min(100.0, float(alert_raw))

        # Factor 2: Dynamic Flight State Complexity (0 to 100)
        # Proportion of climbing/descending vs level flights
        dynamic_rates = 0
        for p in airborne_aircraft:
            vr = p.get("vertical_rate")
            if vr is not None and abs(vr) > 2.5:  # > ~500 ft/min
                dynamic_rates += 1

        dynamic_ratio = (dynamic_rates / airborne_count) if airborne_count > 0 else 0.0
        state_score = min(100.0, (dynamic_ratio * 70.0) + (min(airborne_count, 50) * 0.6))

        # Factor 3: Weather Complexity (0 to 100)
        wx_score = 10.0  # baseline nominal VFR
        if weather_reports:
            adverse_count = 0
            for w in weather_reports:
                cat = w.get("flight_category", "VFR")
                has_cb = w.get("has_cumulonimbus", False)
                wx_str = w.get("weather_string", "")
                if cat in ("LIFR", "IFR") or "TS" in wx_str or has_cb:
                    adverse_count += 3
                elif cat == "MVFR" or (w.get("wind_gust_kt") and w.get("wind_gust_kt") > 20):
                    adverse_count += 1
            wx_ratio = adverse_count / (len(weather_reports) * 3)
            wx_score = min(100.0, (wx_ratio * 90.0) + 10.0)

        # Factor 4: Telemetry Uncertainty (0 to 100)
        missing_count = 0
        for p in airborne_aircraft:
            if p.get("baro_altitude") is None or p.get("heading") is None or p.get("velocity") is None:
                missing_count += 1
        uncertainty_ratio = (missing_count / airborne_count) if airborne_count > 0 else 0.0
        uncertainty_score = min(100.0, uncertainty_ratio * 100.0)

        # Composite Weighted Index (0 - 100)
        composite_index = (
            (alert_score * 0.40)
            + (state_score * 0.25)
            + (wx_score * 0.20)
            + (uncertainty_score * 0.15)
        )
        composite_index = max(5.0, min(100.0, round(composite_index, 1)))

        # Qualitative Level
        if composite_index >= 75:
            level = "CRITICAL"
            level_desc = "Severe Information Overload Potential — Multiple high-priority operational anomalies"
        elif composite_index >= 50:
            level = "HIGH"
            level_desc = "Elevated Cognitive Workload — Multiple attention items and complex operational conditions"
        elif composite_index >= 28:
            level = "MEDIUM"
            level_desc = "Moderate Workload — Routine monitoring with localized attention requirements"
        else:
            level = "LOW"
            level_desc = "Nominal Airspace — Smooth operational environment, low information density"

        # Contributing breakdown
        contributing_factors = [
            {
                "factor": "Alert Prioritization Load",
                "score": round(alert_score, 1),
                "weight": "40%",
                "details": f"{len(alerts)} total alerts ({critical_count} Critical, {high_count} High, {medium_count} Med)",
            },
            {
                "factor": "Flight Profile Dynamics",
                "score": round(state_score, 1),
                "weight": "25%",
                "details": f"{dynamic_rates} aircraft in active climb/descent out of {airborne_count} airborne",
            },
            {
                "factor": "Meteorological Complexity",
                "score": round(wx_score, 1),
                "weight": "20%",
                "details": f"{len(weather_reports)} stations monitored for convective/IFR activity",
            },
            {
                "factor": "Telemetry Uncertainty",
                "score": round(uncertainty_score, 1),
                "weight": "15%",
                "details": f"{missing_count} aircraft with missing altitude/heading vectors",
            },
        ]

        return {
            "workload_index": composite_index,
            "level": level,
            "level_description": level_desc,
            "total_aircraft": total_aircraft,
            "airborne_count": airborne_count,
            "total_alerts": len(alerts),
            "critical_alerts": critical_count,
            "high_alerts": high_count,
            "medium_alerts": medium_count,
            "low_alerts": low_count,
            "contributing_factors": contributing_factors,
            "alert_score": alert_score,
            "state_score": state_score,
            "weather_score": wx_score,
            "uncertainty_score": uncertainty_score,
            "disclaimer": "AI-Assisted Workload Indicator — Research Prototype. Derived from observable data complexity.",
        }

    # ============================================================
    # 2. AI SITUATION AWARENESS SUMMARY
    # ============================================================

    def generate_situation_summary(
        self,
        aircraft_list: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        weather_reports: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generates natural language AI Situation Awareness overview from current real data.
        """
        monitored_total = len(aircraft_list)
        airborne_total = sum(1 for p in aircraft_list if not p.get("on_ground", False))
        ground_total = monitored_total - airborne_total
        weather_count = len(weather_reports)
        attention_count = len(alerts)

        crit_alerts = [a for a in alerts if a.get("priority") == "CRITICAL"]
        high_alerts = [a for a in alerts if a.get("priority") == "HIGH"]

        # If OpenAI client is available, try to produce an executive synthesis
        llm_summary = None
        if self.client:
            try:
                system_prompt = (
                    "You are AeroGuardian AI, an academic aviation decision-support agent. "
                    "Analyze real airspace data concisely (3-4 sentences). "
                    "Emphasize attention items, flight safety buffer, and human-factor workload. "
                    "Never claim aircraft are definitively dangerous; use cautious phrasing: "
                    "'Potential concern detected', 'Requires attention', 'Further verification recommended'. "
                    "Never issue flight control commands."
                )
                user_content = (
                    f"Current Real Airspace Snapshot:\n"
                    f"- Total Aircraft: {monitored_total} ({airborne_total} airborne, {ground_total} on ground)\n"
                    f"- Weather Stations Monitored: {weather_count}\n"
                    f"- Active Attention Alerts: {attention_count}\n"
                    f"- Critical Alerts: {[a['alert_title'] + ' for ' + a['callsign'] for a in crit_alerts[:3]]}\n"
                    f"- High Alerts: {[a['alert_title'] + ' for ' + a['callsign'] for a in high_alerts[:3]]}\n"
                    f"Provide an executive operational situation awareness summary."
                )
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    max_tokens=220,
                    temperature=0.3,
                )
                llm_summary = response.choices[0].message.content.strip()
            except Exception:
                llm_summary = None

        # Robust Heuristic / Rule-based Summary Fallback
        if not llm_summary:
            if crit_alerts:
                highest_title = crit_alerts[0]["alert_title"]
                highest_callsign = crit_alerts[0]["callsign"]
                llm_summary = (
                    f"The current monitored environment contains urgent operational conditions requiring immediate "
                    f"situational review. In particular, {highest_title} for aircraft {highest_callsign} warrants "
                    f"priority verification. Of {monitored_total} monitored flights ({airborne_total} airborne), "
                    f"{attention_count} total items require attention across flight profiles and terminal weather."
                )
            elif high_alerts:
                highest_title = high_alerts[0]["alert_title"]
                highest_callsign = high_alerts[0]["callsign"]
                llm_summary = (
                    f"Elevated attention conditions detected in the monitored airspace. Aircraft {highest_callsign} "
                    f"presents a potential concern ({highest_title}). Environmental and state vectors across "
                    f"{airborne_total} airborne aircraft are being tracked, with {attention_count} active items "
                    f"prioritized to mitigate information overload."
                )
            elif attention_count > 0:
                llm_summary = (
                    f"Nominal traffic flow observed across {monitored_total} monitored aircraft ({airborne_total} airborne). "
                    f"{attention_count} minor operational observations detected, primarily involving routine telemetry "
                    f"vectors or local terminal weather. Standard vigilance is recommended."
                )
            else:
                llm_summary = (
                    f"All {monitored_total} monitored aircraft ({airborne_total} airborne) are operating within nominal "
                    f"parameters. Monitored weather stations show stable terminal conditions with zero anomalous "
                    f"state vectors detected."
                )

        return {
            "aircraft_monitored": monitored_total,
            "aircraft_airborne": airborne_total,
            "aircraft_ground": ground_total,
            "weather_stations": weather_count,
            "active_attention_items": attention_count,
            "summary_text": llm_summary,
        }

    # ============================================================
    # 3. EXPLAINABLE REASONING FOR SELECTED AIRCRAFT
    # ============================================================

    def analyze_aircraft_detail(
        self,
        plane: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        weather_reports: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Produces deep explainable reasoning for a specific selected aircraft.
        """
        callsign = plane.get("callsign", "N/A")
        icao24 = plane.get("icao24", "Unknown")
        plane_alerts = [a for a in alerts if a.get("icao24") == icao24]

        # Determine overall attention tier for this aircraft
        if any(a["priority"] == "CRITICAL" for a in plane_alerts):
            tier = "CRITICAL"
            badge = "Immediate attention recommended"
        elif any(a["priority"] == "HIGH" for a in plane_alerts):
            tier = "HIGH"
            badge = "Important situation requiring attention"
        elif any(a["priority"] == "MEDIUM" for a in plane_alerts):
            tier = "MEDIUM"
            badge = "Monitor situation"
        elif plane_alerts:
            tier = "LOW"
            badge = "Informational observation"
        else:
            tier = "NORMAL"
            badge = "Nominal flight parameters"

        # Check for missing fields
        missing_fields = []
        for k in ["baro_altitude", "velocity", "heading", "vertical_rate", "squawk", "geo_altitude"]:
            if plane.get(k) is None:
                missing_fields.append(k)

        data_completeness = round(((7 - len(missing_fields)) / 7.0) * 100, 0)

        # Observations & Reasoning
        observations = []
        for a in plane_alerts:
            observations.append(
                {
                    "title": a["alert_title"],
                    "priority": a["priority"],
                    "what_detected": a["detected"],
                    "why_it_matters": a["why_it_matters"],
                    "trigger_data": a["triggering_data"],
                    "confidence": a["confidence"],
                    "suggested_action": a["suggested_verification"],
                }
            )

        if not observations:
            observations.append(
                {
                    "title": "Nominal Flight State",
                    "priority": "LOW",
                    "what_detected": "Aircraft state vector conforms to standard altitude, velocity, and transponder ranges.",
                    "why_it_matters": "No operational hazards or attention-worthy anomalies identified in received telemetry.",
                    "trigger_data": f"Altitude: {plane.get('baro_altitude') or 'N/A'} m, Speed: {plane.get('velocity') or 'N/A'} m/s",
                    "confidence": "High (Direct OpenSky ADS-B Vector)",
                    "suggested_action": "Continue routine situational monitoring.",
                }
            )

        return {
            "callsign": callsign,
            "icao24": icao24,
            "country": plane.get("country", "Unknown"),
            "attention_tier": tier,
            "attention_badge": badge,
            "data_completeness_pct": data_completeness,
            "missing_fields": missing_fields,
            "observations": observations,
            "alert_count": len(plane_alerts),
        }

    # ============================================================
    # 4. GROUNDED AI ASSISTANT (Q&A & AIRCRAFT REASONING)
    # ============================================================

    def find_aircraft_in_query(
        self, query: str, aircraft_list: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Find a specific aircraft by callsign, ICAO24, or registration, avoiding common stop words."""
        STOP_WORDS = {
            "THE", "ALL", "AND", "FOR", "WITH", "ABOUT", "DETAILS", "RELATED", "AEROPLANE", "AIRPLANE",
            "AIRCRAFT", "FLIGHT", "FLIGHTS", "TELL", "SHOW", "WHAT", "WHICH", "GIVE", "IMPROVE",
            "ASSISTANT", "PLEASE", "INFO", "INFORMATION", "DATA", "STATUS", "REPORT", "FIND", "VIEW",
            "NEAR", "FASTEST", "HIGHEST", "LOWEST", "SPEED", "ALTITUDE", "EVERYTHING", "KNOW", "EXPLAIN",
            "SYSTEM", "SYSTEMS", "CHECKLIST", "CHECKLISTS", "PILOT", "AIRPORT", "WEATHER"
        }
        tokens = re.findall(r"[a-zA-Z0-9_\-]+", query)
        candidate_tokens = [t for t in tokens if t.upper() not in STOP_WORDS and len(t) >= 3]

        # 1. Exact Callsign Match (case-insensitive)
        for tok in candidate_tokens:
            tok_upper = tok.upper()
            for p in aircraft_list:
                cs = (p.get("callsign") or "").upper().strip()
                if cs and cs == tok_upper:
                    return p

        # 2. Exact ICAO 24-bit Hex Match (typically 6 hex digits, e.g. "800c0b", "a7e310")
        for tok in candidate_tokens:
            tok_lower = tok.lower()
            for p in aircraft_list:
                hex_code = (p.get("icao24") or "").lower().strip()
                if hex_code and hex_code == tok_lower:
                    return p

        # 3. Exact Tail Registration Match (e.g. "VT-BWA", "N607UP")
        for tok in candidate_tokens:
            tok_upper = tok.upper()
            for p in aircraft_list:
                reg = (p.get("registration") or "").upper().strip()
                if reg and reg == tok_upper:
                    return p

        # 4. Partial / Substring Match for tokens of 4+ characters with digits (like "AIC101", "UPS15", "607UP")
        for tok in candidate_tokens:
            if len(tok) >= 4 and any(c.isdigit() for c in tok):
                tok_upper = tok.upper()
                for p in aircraft_list:
                    cs = (p.get("callsign") or "").upper().strip()
                    if cs and tok_upper in cs:
                        return p

        return None

    def format_aeroplane_full_details(
        self,
        plane: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        weather_reports: List[Dict[str, Any]],
    ) -> str:
        """
        Produces an exhaustive, cockpit-grade operational report of ALL
        parameters and details related to an aeroplane.
        """
        callsign = plane.get("callsign") or "N/A"
        icao24 = plane.get("icao24") or "Unknown"
        country = plane.get("country") or "Unknown"
        ac_type = plane.get("aircraft_type") or "Commercial Aircraft"
        reg = plane.get("registration")
        reg_str = f" • Tail Registration: `{reg}`" if reg else ""

        # Altitude & Flight Level
        alt_m = plane.get("baro_altitude")
        alt_ft = plane.get("altitude_ft") or (int(meters_to_feet(alt_m)) if alt_m is not None else None)
        fl_str = plane.get("flight_level") or (f"FL{round(alt_ft / 100)}" if alt_ft is not None else "N/A")
        alt_display = f"**{fl_str}** ({alt_ft:,} ft MSL / {round(alt_m):,} m)" if alt_ft is not None else "N/A"

        # Speed & Aerodynamics
        v_ms = plane.get("velocity")
        spd_kts = plane.get("speed_kts") or (round(ms_to_knots(v_ms)) if v_ms is not None else None)
        spd_kmh = plane.get("speed_kmh") or (round(ms_to_kmh(v_ms)) if v_ms is not None else None)
        mach = plane.get("mach") or estimate_mach(v_ms, alt_m)
        mach_str = f"Mach {mach}" if mach is not None else "Sub-Mach"

        # Vertical Speed Indicator
        vr_ms = plane.get("vertical_rate")
        vr_fpm = plane.get("vertical_rate_fpm") or (round(ms_to_ft_per_min(vr_ms)) if vr_ms is not None else None)
        if vr_fpm is not None:
            if abs(vr_fpm) < 150:
                vr_status = "LEVEL FLIGHT"
                vr_display = f"{vr_fpm:+d} FPM ({vr_status})"
            elif vr_fpm > 0:
                vr_status = "CLIMBING"
                vr_display = f"▲ +{vr_fpm:,} FPM ({vr_status})"
            else:
                vr_status = "DESCENDING"
                vr_display = f"▼ {vr_fpm:,} FPM ({vr_status})"
        else:
            vr_display = "N/A"

        # Track & Heading
        hdg = plane.get("heading")
        if hdg is not None:
            dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
            idx = int((hdg + 11.25) / 22.5) % 16
            hdg_display = f"{round(hdg)}° ({dirs[idx]})"
        else:
            hdg_display = "N/A"

        # Geographic Coordinates
        lat = plane.get("latitude")
        lon = plane.get("longitude")
        coord_str = f"{lat:.4f}° N, {lon:.4f}° E" if lat is not None and lon is not None else "N/A"

        # Operational Status & Squawk
        on_ground = plane.get("on_ground", False)
        status_str = "Surface (On Ground / Taxiway)" if on_ground else "Airborne in Controlled Airspace"
        squawk = plane.get("squawk") or "N/A"
        is_emergency = squawk in ("7700", "7600", "7500")

        # Flight Lifecycle Phase
        phase_info = plane.get("flight_phase") or classify_flight_phase(plane)
        if isinstance(phase_info, dict):
            phase_name = phase_info.get("phase", "NOMINAL AIRBORNE")
            phase_desc = phase_info.get("description", "Standard flight operations.")
            phase_code = phase_info.get("code", "LEVEL")
        else:
            phase_name = str(phase_info)
            phase_desc = "Standard flight operations."
            phase_code = "LEVEL"

        # Wake Turbulence Separation Category
        wake = plane.get("wake_category") or get_wake_category(plane.get("category"))
        if isinstance(wake, dict):
            wake_desc = wake.get("description", "Standard Wake Separation")
            wake_code = wake.get("code", "M")
        else:
            wake_desc = str(wake)
            wake_code = "M"

        # Nearest Aerodrome & Crosswind Vector
        nearest = plane.get("nearest_airport")
        nearest_section = ""
        if nearest and isinstance(nearest, dict):
            cross_badge = " ⚠️ HIGH CROSSWIND CAUTION" if (nearest.get("crosswind_kt") or 0) > 15 else ""
            tail_badge = " (Tailwind Alert)" if nearest.get("is_tailwind") else ""
            nearest_section = (
                f"\n#### 4. Nearest Aerodrome Proximity & Crosswind Vector\n"
                f"- **Nearest Aerodrome Hub**: **{nearest.get('icao')}** ({nearest.get('name')})\n"
                f"- **Distance & Relative Bearing**: **{nearest.get('distance_nm')} NM** on **{nearest.get('bearing_deg')}° Track**\n"
                f"- **Terminal Flight Rules**: `{nearest.get('flight_category', 'VFR')}` (METAR Verified)\n"
                f"- **Surface Wind**: `{nearest.get('wind_speed_kt', 0)} kts @ {nearest.get('wind_dir_deg', 0)}°`\n"
                f"- **Runway Crosswind Component**: **{nearest.get('crosswind_kt', 0)} kts** {nearest.get('crosswind_dir', '')}{cross_badge}\n"
                f"- **Axial Wind Component**: **{abs(nearest.get('headwind_kt', 0))} kts** {'TAILWIND' if nearest.get('is_tailwind') else 'HEADWIND'}{tail_badge}\n"
            )

        # Alerts & Observations
        plane_alerts = [a for a in alerts if a.get("icao24") == icao24]
        if plane_alerts:
            alert_items = "\n".join([f"  * **[{a['priority']}] {a['alert_title']}**: {a['detected']} (Recommended Action: *{a['suggested_verification']}*)" for a in plane_alerts])
            safety_section = f"\n#### 5. AI Guardian Safety Diagnostic\n⚠️ **{len(plane_alerts)} Active Attention Items Detected:**\n{alert_items}\n"
        else:
            safety_section = (
                f"\n#### 5. AI Guardian Safety Diagnostic\n"
                f"✅ **Nominal Flight Parameters**: Mode-S telemetry indicates the aircraft is operating within standard aerodynamic, altitude, and separation limits.\n"
            )

        # Contextual Decision-Support Checklist
        if phase_code == "GROUND":
            checklist_items = [
                "Verify ATC taxi route clearance and assigned departure runway",
                "Confirm transponder set to assigned departure squawk code",
                "Review departure aerodrome ATIS / METAR and altimeter setting (QNH)",
                "Cross-check departure runway surface condition and crosswind limits",
            ]
        elif phase_code in ("TAKEOFF", "CLIMB"):
            checklist_items = [
                "Monitor initial climb speed and pitch limit margins",
                "Verify transition altitude altimeter setting (Standard 1013.2 hPa / 29.92 inHg)",
                "Confirm climb clearance to en-route cruise flight level",
                "Check engine climb thrust rating and airspeed acceleration",
            ]
        elif phase_code == "CRUISE":
            checklist_items = [
                "Cross-check cruise Mach number and aerodynamic buffet margin",
                "Compare actual fuel burn versus flight plan scheduled burn rate",
                "Review high-altitude jet stream and CAT (Clear Air Turbulence) SIGMETs",
                "Identify nearest suitable en-route diversion aerodromes & runway lengths",
            ]
        elif phase_code == "DESCENT":
            checklist_items = [
                "Obtain latest destination aerodrome ATIS / METAR report",
                "Verify 250 kts speed restriction compliance below 10,000 ft MSL",
                "Cross-check top-of-descent vertical profile and speed brake deployment",
                "Brief descent arrival routing and Minimum Safe Altitude (MSA)",
            ]
        elif phase_code == "APPROACH":
            checklist_items = [
                "Confirm stabilized approach criteria met before 1,000 ft AGL",
                "Verify runway surface wind and calculated crosswind component",
                "Confirm missed approach / go-around altitude and missed approach procedure briefed",
                "Check landing gear down-and-locked and flap configuration",
            ]
        else:
            checklist_items = [
                "Verify assigned flight level and heading vector adherence",
                "Monitor airspeed margin and fuel remaining",
                "Maintain continuous watch on transponder squawk code",
            ]

        checklist_str = "\n".join([f"- [ ] {item}" for item in checklist_items])

        return (
            f"### ✈️ Complete Aeroplane Operational & Telemetry Report: **{callsign}** (`{icao24}`)\n\n"
            f"#### 1. Aircraft Airframe & Identification\n"
            f"- **Flight Callsign**: `{callsign}`\n"
            f"- **ICAO 24-bit Transponder Hex**: `0x{icao24.upper()}`\n"
            f"- **Country of Origin**: {country}\n"
            f"- **Aircraft Type / Model**: {ac_type}{reg_str}\n"
            f"- **Wake Turbulence Separation Category**: **{wake_desc}** (`WAKE: {wake_code}`)\n"
            f"- **Transponder Squawk**: `{squawk}` {'🚨 EMERGENCY SQUAWK' if is_emergency else '(Discrete Mode 3/A Code)'}\n"
            f"- **Operational Status**: {status_str}\n\n"
            f"#### 2. Flight Deck Avionics & Aerodynamics\n"
            f"- **Barometric Altitude**: {alt_display}\n"
            f"- **Calibrated Airspeed**: **{spd_kts or 'N/A'} KTS** ({spd_kmh or 'N/A'} km/h / {round(v_ms, 1) if v_ms else 'N/A'} m/s)\n"
            f"- **Aerodynamic Velocity**: **{mach_str}** ($M = V / a(h)$)\n"
            f"- **Vertical Speed (VSI)**: **{vr_display}**\n"
            f"- **True Heading / Track**: **{hdg_display}**\n"
            f"- **Geographic Coordinates**: `{coord_str}`\n\n"
            f"#### 3. Flight Lifecycle Phase\n"
            f"- **Classified Lifecycle Phase**: **{phase_name}**\n"
            f"- **Operational Envelope**: {phase_desc}\n"
            f"{nearest_section}"
            f"{safety_section}\n"
            f"#### 6. Contextual Decision-Support Checklist ({phase_name})\n"
            f"{checklist_str}"
        )

    def answer_query(
        self,
        query: str,
        aircraft_list: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        weather_reports: List[Dict[str, Any]],
        workload_info: Dict[str, Any],
    ) -> str:
        """
        Answers user inquiries grounded strictly on the live telemetry, weather, and alerts.
        Provides exhaustive details for any specific flight or general aeroplane queries.
        """
        q_lower = query.lower().strip()

        # 1. Check if user query matches any specific aircraft callsign, icao24, or registration
        matched_plane = self.find_aircraft_in_query(query, aircraft_list)
        if matched_plane:
            return self.format_aeroplane_full_details(matched_plane, alerts, weather_reports)

        # 2. Check for superlative aircraft queries: "fastest", "highest", "lowest"
        if ("fastest" in q_lower or "max speed" in q_lower or "top speed" in q_lower) and aircraft_list:
            fastest = max(aircraft_list, key=lambda p: p.get("velocity") or 0)
            report = self.format_aeroplane_full_details(fastest, alerts, weather_reports)
            return f"**Fastest Aircraft Detected in Monitored Airspace:**\n\n" + report

        if ("highest" in q_lower or "max altitude" in q_lower or "top altitude" in q_lower or "highest cruise" in q_lower) and aircraft_list:
            airborne = [p for p in aircraft_list if p.get("baro_altitude")]
            if airborne:
                highest = max(airborne, key=lambda p: p.get("baro_altitude") or 0)
                report = self.format_aeroplane_full_details(highest, alerts, weather_reports)
                return f"**Highest Altitude Flight in Monitored Airspace:**\n\n" + report

        # 3. Check for general "all details of aeroplane" / "aeroplane details" query
        is_general_plane_query = any(term in q_lower for term in [
            "all details",
            "details related to aeroplane",
            "details of aeroplane",
            "aeroplane details",
            "airplane details",
            "aircraft details",
            "about aeroplane",
            "about airplane",
            "related to aeroplane",
            "tell about aeroplane",
            "tell me about aeroplane",
            "aeroplane",
            "airplane",
            "improve the ai",
            "aircraft systems",
            "how does an aeroplane work",
            "how does an airplane work",
            "what are the parts of an aeroplane",
        ])

        if is_general_plane_query and aircraft_list:
            # Pick the most prominent airborne aircraft for a live demonstration
            airborne_planes = [p for p in aircraft_list if not p.get("on_ground", False) and p.get("baro_altitude")]
            sample_plane = max(airborne_planes, key=lambda p: p.get("baro_altitude") or 0) if airborne_planes else aircraft_list[0]

            overview = (
                "### ✈️ Complete Aeroplane Engineering, Aerodynamics & Operational Guide\n\n"
                "An aeroplane is a complex, multi-system aerospace vehicle designed to operate safely within the earth's atmosphere. "
                "AeroGuardian AI monitors and computes every aerodynamic and operational dimension in real time from Mode-S ADS-B Extended Squitter transponder telemetry:\n\n"
                "#### 1. Fundamental Aerodynamics (The Four Forces of Flight)\n"
                "- **Lift ($L$)**: Upward aerodynamic force created by airfoils (wings) via Bernoulli's pressure differential and Newtonian downwash deflection ($L = 0.5 \\cdot \\rho \\cdot v^2 \\cdot S \\cdot C_L$).\n"
                "- **Weight ($W$)**: Downward gravitational force acting through the Center of Gravity (CG), balanced by lift in steady level flight ($L = W$).\n"
                "- **Thrust ($T$)**: Forward propulsive force generated by turbofan/turboprop engines overcoming aerodynamic drag ($T = D$ at constant speed).\n"
                "- **Drag ($D$)**: Retarding aerodynamic resistance consisting of **Parasite Drag** (skin friction, form drag) and **Induced Drag** (tip vortex drag resulting from lift generation).\n\n"
                "#### 2. Primary Airframe Structure & Flight Control Surfaces\n"
                "- **Fuselage**: Semi-monocoque pressurized cabin accommodating flight crew, passengers, and cargo.\n"
                "- **Primary Flight Controls (Three Axes of Motion)**:\n"
                "  * **Ailerons**: Located on trailing wingtips, control **Roll** around the longitudinal axis.\n"
                "  * **Elevator / Trimmable Horizontal Stabilizer (THS)**: Controls **Pitch** around the lateral axis.\n"
                "  * **Rudder**: Mounted on the vertical fin, controls **Yaw** around the vertical/normal axis.\n"
                "- **High-Lift Devices & Drag Modifiers**:\n"
                "  * **Trailing-Edge Flaps & Leading-Edge Slats**: Extend wing camber and surface area to lower stall speed ($V_{S0}$) for takeoff and landing.\n"
                "  * **Spoilers & Speedbrakes**: Disrupt upper-surface lift for rapid en-route descent and ground rollout wheel-braking efficiency.\n\n"
                "#### 3. Cockpit Avionics & Telemetry Instrumentation\n"
                "- **Primary Flight Display (PFD)**: Displays Attitude (ADI), Calibrated Airspeed tape, Barometric Altitude tape, and Vertical Speed (VSI).\n"
                "- **True Mach Number ($M$)**: Ratio of true airspeed to local speed of sound ($M = V / a$), crucial in the transonic cruise regime ($M 0.74 - 0.86$) to prevent Mach tuck and shock stall.\n"
                "- **Mode-S ADS-B Transponder (1090 MHz)**: Continuously squitters 24-bit ICAO address, flight callsign, pressure altitude (FL), GNSS coordinates, heading, and discrete squawk code.\n"
                "- **ICAO Wake Turbulence Separation**: Categorized by Maximum Takeoff Weight (MTOW):\n"
                "  * `LIGHT` ($< 7,000$ kg), `MEDIUM` ($7,000 - 136,000$ kg), `HEAVY` ($> 136,000$ kg), and `SUPER` (e.g. Airbus A380 / Antonov An-225).\n\n"
                "#### 4. Flight Lifecycle Phases & Checklists\n"
                "1. **Pre-flight & Taxi**: Altimeter calibration (QNH), surface crosswind review, takeoff flap setting, departure squawk confirmation.\n"
                "2. **Takeoff & Initial Climb**: $V_1$ (takeoff decision speed), $V_R$ (rotation speed), $V_2$ (takeoff safety speed), gear retraction, 250 kts restriction below 10,000 ft MSL.\n"
                "3. **En-Route Cruise**: Transition to Standard Altimeter (1013.25 hPa / 29.92 inHg), Mach speed management, optimum flight level step climbs, fuel burn monitoring.\n"
                "4. **Descent & Terminal Approach**: Top-of-Descent (TOD) calculation (3:1 rule), runway crosswind & tailwind computation, stabilized approach criteria by 1,000 ft AGL.\n\n"
                "---\n\n"
            )
            live_report = self.format_aeroplane_full_details(sample_plane, alerts, weather_reports)
            return overview + f"#### 5. Real-Time Monitored Aircraft Telemetry Inspection ({len(aircraft_list)} Flights in Airspace)\n" + live_report

        # 4. If OpenAI client is ready, prompt LLM with exact live context
        if self.client:
            try:
                context_str = (
                    f"REAL Monitored Airspace Context:\n"
                    f"- Total Aircraft: {len(aircraft_list)}\n"
                    f"- Airborne: {sum(1 for p in aircraft_list if not p.get('on_ground', False))}\n"
                    f"- Workload Index: {workload_info.get('workload_index')}% ({workload_info.get('level')})\n"
                    f"- Total Alerts: {len(alerts)}\n"
                    f"- Sample Aircraft Details:\n"
                )
                for p in aircraft_list[:4]:
                    nearest = p.get("nearest_airport") or {}
                    context_str += (
                        f"  * Flight {p.get('callsign')} ({p.get('icao24')}, {p.get('country')}): "
                        f"Alt={p.get('flight_level')} ({p.get('altitude_ft')} ft), Spd={p.get('speed_kts')} kts (M {p.get('mach')}), "
                        f"VSI={p.get('vertical_rate_fpm')} fpm, Hdg={p.get('heading')} deg, Phase={p.get('flight_phase', {}).get('phase')}, "
                        f"Wake={p.get('wake_category', {}).get('category')}, Nearest={nearest.get('icao')} ({nearest.get('distance_nm')} NM, X-Wind={nearest.get('crosswind_kt')} kts)\n"
                    )

                context_str += "- Active Alerts Summary:\n"
                for a in alerts[:6]:
                    context_str += f"  * [{a['priority']}] {a['callsign']} ({a['icao24']}): {a['alert_title']} - {a['detected']}\n"

                system_msg = (
                    "You are AeroGuardian AI Assistant, an advanced aviation decision-support specialist. "
                    "When asked about an aeroplane or aircraft details, provide a comprehensive, structured briefing "
                    "covering: 1. Identification & Airframe (Callsign, ICAO, Country, Wake Category), "
                    "2. Cockpit Avionics & Aerodynamics (Airspeed, Mach, Flight Level, VSI, Heading), "
                    "3. Flight Lifecycle Phase, 4. Nearest Aerodrome Distance & Runway Crosswind Component, "
                    "5. Safety Diagnostics, and 6. Procedural Decision-Support Checklists. "
                    "Answer strictly using the real provided telemetry, weather, and alerts context. "
                    "Never invent data. Use academic caution ('Potential concern detected', 'Verification recommended')."
                )

                resp = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"{context_str}\n\nUser Question: {query}"},
                    ],
                    max_tokens=600,
                    temperature=0.2,
                )
                return resp.choices[0].message.content.strip()
            except Exception:
                pass

        # 5. Robust Heuristic / Context Grounded Fallback Engine
        if "what aircraft" in q_lower or "monitored" in q_lower or "how many aircraft" in q_lower:
            airborne = sum(1 for p in aircraft_list if not p.get("on_ground", False))
            countries = set(p.get("country", "") for p in aircraft_list if p.get("country"))
            sample_callsigns = [p.get("callsign") for p in aircraft_list if p.get("callsign") and p.get("callsign") != "N/A"][:8]
            return (
                f"Currently, AeroGuardian AI is actively monitoring **{len(aircraft_list)} real aircraft** "
                f"({airborne} airborne and {len(aircraft_list) - airborne} on-ground) across "
                f"**{len(countries)} countries of registration**.\n\n"
                f"Sample active callsigns: {', '.join(sample_callsigns) if sample_callsigns else 'None'}.\n"
                f"All position coordinates, barometric altitudes, Mach numbers, and tracks are fetched directly from live ADS-B / Mode-S transponder streams."
            )

        elif "require attention" in q_lower or "which aircraft" in q_lower or "attention" in q_lower:
            if not alerts:
                return "At present, **no aircraft** exhibit anomalous flight profiles or emergency transponder codes in the monitored airspace."
            crit_high = [a for a in alerts if a["priority"] in ("CRITICAL", "HIGH")]
            lines = [f"**{len(alerts)} aircraft attention items** are currently prioritized:"]
            for a in (crit_high if crit_high else alerts)[:6]:
                lines.append(f"- **{a['callsign']}** (`{a['icao24']}`): **[{a['priority']}]** {a['alert_title']} - *{a['detected']}*")
            lines.append("\nSuggested action: Review these flights on the Live Aircraft Map or Alert Center for suggested verifications.")
            return "\n".join(lines)

        elif "highest priority" in q_lower or "explain the highest" in q_lower or "top alert" in q_lower:
            if not alerts:
                return "There are currently no active alerts. All monitored flights are operating within nominal criteria."
            top = alerts[0]
            return (
                f"### Highest Priority Alert: **{top['alert_title']}**\n\n"
                f"- **Priority Tier**: `{top['priority']}`\n"
                f"- **Target Flight**: `{top['callsign']}` (ICAO24: `{top['icao24']}`)\n"
                f"- **Condition Detected**: {top['detected']}\n"
                f"- **Operational Impact**: {top['why_it_matters']}\n"
                f"- **Triggering Telemetry**: `{top['triggering_data']}`\n"
                f"- **Confidence Assessment**: {top['confidence']}\n"
                f"- **Recommended Verification**: {top['suggested_verification']}"
            )

        elif "metar" in q_lower or "weather" in q_lower or any(code in q_lower for code in ["vidp", "vobl", "vabb", "vohs", "vecc", "vomm"]):
            if not weather_reports:
                return "No weather station reports have been queried yet. Please visit the Aviation Weather tab to inspect METAR/TAF data."
            lines = [f"### Monitored Aviation Weather Overview ({len(weather_reports)} Stations):"]
            for w in weather_reports[:4]:
                lines.append(
                    f"- **{w['icao']}** ({w.get('name')}): Flight Category **{w.get('flight_category')}** | "
                    f"Wind: {w.get('wind_dir_deg', 'N/A')}° at {w.get('wind_speed_kt', 'N/A')} kts | "
                    f"Vis: {w.get('visibility_sm', 'N/A')} SM | Temp: {w.get('temperature_c', 'N/A')}°C | "
                    f"WX: {w.get('weather_string', 'None')}\n"
                    f"  `{w.get('raw_text')}`"
                )
            return "\n\n".join(lines)

        elif "workload" in q_lower or "elevated" in q_lower or "indicator" in q_lower:
            score = workload_info.get("workload_index", 0)
            level = workload_info.get("level", "LOW")
            factors = workload_info.get("contributing_factors", [])
            factor_text = "\n".join([f"- **{f['factor']}** ({f['weight']}): Score {f['score']}/100 — {f['details']}" for f in factors])
            return (
                f"### AI-Assisted Workload Indicator: **{score}% ({level})**\n\n"
                f"This indicator models environmental and information density to help prevent pilot and controller overload. "
                f"It is a **research prototype** calculated strictly from observable parameters:\n\n"
                f"{factor_text}\n\n"
                f"*Note: This research prototype does not measure psychological fatigue or claim clinical validation.*"
            )

        elif "wake" in q_lower or "vortex" in q_lower:
            return (
                "### 🌪️ ICAO Wake Turbulence Separation Standards\n\n"
                "Wake turbulence consists of counter-rotating wingtip vortices generated whenever an aeroplane creates aerodynamic lift. "
                "Strength is proportional to aircraft weight and inversely proportional to wingspan and speed.\n\n"
                "#### ICAO Wake Categories & Trailing Distance Minimums:\n"
                "- **SUPER (`J`)**: Airbus A380-800, Antonov An-225 (MTOW >= 560,000 kg). Trailing separation: **6 to 8 NM**.\n"
                "- **HEAVY (`H`)**: All aircraft of MTOW >= 136,000 kg (Boeing 747, 777, 787, Airbus A330, A350). Trailing separation: **4 to 6 NM**.\n"
                "- **MEDIUM (`M`)**: Aircraft between 7,000 kg and 136,000 kg (Boeing 737, Airbus A320, Embraer E190). Trailing separation: **3 to 5 NM**.\n"
                "- **LIGHT (`L`)**: Aircraft of MTOW <= 7,000 kg (Cessna 172, Beechcraft, light twins). Trailing separation: **4 to 6 NM** behind heavier traffic."
            )

        elif "squawk" in q_lower or "transponder" in q_lower or any(c in q_lower for c in ["7700", "7600", "7500"]):
            return (
                "### 📡 Mode 3/A Transponder Squawk Codes & Emergency Protocol\n\n"
                "A squawk code is a 4-digit octal number (0000 to 7777, digits 0-7) assigned by Air Traffic Control (ATC) "
                "for secondary surveillance radar (SSR) identification.\n\n"
                "#### Critical ICAO Aviation Emergency Squawks:\n"
                "- **`7500` — Unlawful Interference / Hijacking**: Silently alerts ATC that the flight deck is compromised without alarming cabin occupants.\n"
                "- **`7600` — Radio Communication Failure (Lost Comms)**: Notifies ATC that the aircraft cannot transmit or receive voice VHF transmissions. Pilot follows standard lost comms IFR clearance protocol.\n"
                "- **`7700` — General In-Flight Emergency**: Declares an immediate distress situation (Mayday/Pan-Pan) due to engine failure, cabin depressurization, medical emergency, or structural damage.\n\n"
                "#### Standard Conspicuity Squawks:\n"
                "- **`1200`**: Standard VFR (Visual Flight Rules) in North America.\n"
                "- **`7000`**: Standard VFR in European / ICAO airspace.\n"
                "- **`2000`**: Unassigned IFR oceanic or trans-border entry."
            )

        elif "mach" in q_lower or "speed of sound" in q_lower:
            return (
                "### 🚀 Aerodynamic Mach Number (M)\n\n"
                "Mach number is the ratio of true airspeed (V) to the local speed of sound (a):\n"
                "$$M = V / a$$\n\n"
                "The speed of sound decreases with altitude as atmospheric temperature drops (approx. 661 kts at sea level ISA +15°C, decreasing to ~573 kts at the tropopause FL360 -56.5°C).\n\n"
                "- **Subsonic**: M < 0.75\n"
                "- **Transonic**: M 0.75 - 1.20 (standard commercial jet cruise: Boeing 787 at M 0.85, A350 at M 0.85)\n"
                "- **Supersonic**: M 1.20 - 5.0\n"
                "- **Hypersonic**: M > 5.0"
            )

        elif "crosswind" in q_lower:
            return (
                "### 💨 Runway Crosswind & Headwind Calculation\n\n"
                "Aeroplanes must land and take off aligned with the runway center line. Wind blowing at an angle (θ) to the runway heading "
                "is resolved into perpendicular and axial vectors:\n\n"
                "- **Crosswind Component (V_xw)**: V_xw = V_wind * sin(θ)\n"
                "- **Headwind / Tailwind Component (V_hw)**: V_hw = V_wind * cos(θ)\n\n"
                "Most commercial airliners have a Maximum Demonstrated Crosswind limit between **30 and 38 knots** on a dry runway, and **15 to 20 knots** on contaminated (wet/icy) runways."
            )

        else:
            sample_callsign = aircraft_list[0].get("callsign") if aircraft_list else "UPS15"
            return (
                f"I am AeroGuardian AI's aviation decision-support assistant. I have direct visibility into "
                f"the **{len(aircraft_list)} live aircraft** currently tracked via Mode-S / ADS-B and **{len(weather_reports)}** "
                f"weather stations.\n\n"
                f"Ask me anything about aeroplanes, live flight parameters, weather, or safety alerts:\n"
                f"- *'Tell me all details related to aeroplane'*\n"
                f"- *'Tell me all details about flight {sample_callsign}'*\n"
                f"- *'Which aircraft is flying the highest / fastest?'*\n"
                f"- *'What are the emergency transponder squawk codes?'*\n"
                f"- *'How does wake turbulence separation work?'*\n"
                f"- *'Which aircraft require attention?'*\n"
                f"- *'Explain the highest priority alert.'*\n"
                f"- *'What does the VIDP METAR mean?'*"
            )
