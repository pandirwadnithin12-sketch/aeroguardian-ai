"""
AeroGuardian AI - Risk Identification & Anomaly Detection Engine

Evaluates real aircraft state vectors and real weather reports.
Strictly adheres to the no-simulation policy and academic research constraints:
- Uses only real, observable data.
- NEVER issues aircraft flight-control commands or claims to replace pilots/ATC.
- Employs calibrated cautious wording:
    "Potential concern detected"
    "Requires attention"
    "Further verification recommended"
"""

import math
from datetime import datetime
from typing import List, Dict, Any, Optional
from utils import meters_to_feet, ms_to_knots, ms_to_ft_per_min


def calculate_distance_approx(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Approximate great-circle distance between two coordinates in kilometers.
    Equirectangular approximation suitable for terminal area proximity checks.
    """
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat_mid = math.radians((lat1 + lat2) / 2.0)
    x = dlon * math.cos(lat_mid)
    y = dlat
    return math.sqrt(x * x + y * y) * R


def evaluate_aircraft_risk(
    plane: Dict[str, Any],
    weather_reports: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """
    Evaluate a single real aircraft against research risk and anomaly rules.
    Returns a list of structured alert dictionaries.
    """
    alerts: List[Dict[str, Any]] = []

    callsign = plane.get("callsign") or "N/A"
    icao24 = plane.get("icao24") or "Unknown"
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    baro_alt = plane.get("baro_altitude")  # meters
    velocity = plane.get("velocity")        # m/s
    v_rate = plane.get("vertical_rate")    # m/s
    on_ground = plane.get("on_ground", False)
    squawk = plane.get("squawk")
    lat = plane.get("latitude")
    lon = plane.get("longitude")

    alt_ft = meters_to_feet(baro_alt)
    speed_kts = ms_to_knots(velocity)
    v_fpm = ms_to_ft_per_min(v_rate)

    # ------------------------------------------------------------
    # 1. EMERGENCY TRANSPONDER SQUAWK CODES
    # ------------------------------------------------------------
    if squawk:
        sq = str(squawk).strip()
        if sq == "7700":
            alerts.append(
                {
                    "id": f"{icao24}_sq7700_{sq}",
                    "priority": "CRITICAL",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Emergency Squawk Code (7700)",
                    "detected": "Transponder broadcasting international general emergency code (7700).",
                    "why_it_matters": (
                        "Squawk 7700 indicates an ongoing airborne or operational emergency declared by the flight crew. "
                        "Immediate priority handling and situational monitoring is advised."
                    ),
                    "triggering_data": f"Squawk: {sq}, Altitude: {int(alt_ft) if alt_ft else 'N/A'} ft",
                    "confidence": "High (Direct Mode-S Transponder Code)",
                    "suggested_verification": (
                        "Verify emergency declaration with air traffic control. Monitor trajectory, altitude hold, "
                        "and nearest diversion aerodromes."
                    ),
                }
            )
        elif sq == "7600":
            alerts.append(
                {
                    "id": f"{icao24}_sq7600_{sq}",
                    "priority": "CRITICAL",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Radio Failure Squawk Code (7600)",
                    "detected": "Transponder broadcasting two-way radio communications failure code (7600).",
                    "why_it_matters": (
                        "Squawk 7600 signifies loss of air-ground voice communication capability. Standard ICAO lost-comm "
                        "procedures and heightened airspace surveillance apply."
                    ),
                    "triggering_data": f"Squawk: {sq}",
                    "confidence": "High (Direct Mode-S Transponder Code)",
                    "suggested_verification": (
                        "Verify alternate communication frequencies, standard routing adherence, and visual ATC signals."
                    ),
                }
            )
        elif sq == "7500":
            alerts.append(
                {
                    "id": f"{icao24}_sq7500_{sq}",
                    "priority": "CRITICAL",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Unlawful Interference Squawk Code (7500)",
                    "detected": "Transponder broadcasting unlawful interference code (7500).",
                    "why_it_matters": "Squawk 7500 indicates potential security threat or unlawful intervention on board.",
                    "triggering_data": f"Squawk: {sq}",
                    "confidence": "High (Direct Mode-S Transponder Code)",
                    "suggested_verification": "Immediate notification to relevant civil aviation security authorities.",
                }
            )

    # ------------------------------------------------------------
    # 2. EXTREME VERTICAL RATES (AIRBORNE)
    # ------------------------------------------------------------
    if not on_ground and v_fpm is not None:
        if v_fpm < -5000:
            alerts.append(
                {
                    "id": f"{icao24}_descent_crit",
                    "priority": "CRITICAL",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Severe High-Rate Descent Detected",
                    "detected": f"Aircraft vertical descent rate is {int(round(v_fpm)):,} ft/min.",
                    "why_it_matters": (
                        "Descent rates exceeding 5,000 ft/min are atypical for commercial flight profiles and may "
                        "indicate an emergency depressurization descent, abrupt altitude loss, or flight path anomaly."
                    ),
                    "triggering_data": f"Vertical rate: {int(round(v_fpm)):,} ft/min ({v_rate:.1f} m/s), Altitude: {int(round(alt_ft)) if alt_ft else 'N/A'} ft",
                    "confidence": "High (ADS-B State Vector)",
                    "suggested_verification": (
                        "Check cleared flight level, rate trend over consecutive sweeps, and proximity to minimum safe altitude (MSA)."
                    ),
                }
            )
        elif v_fpm < -3000:
            alerts.append(
                {
                    "id": f"{icao24}_descent_high",
                    "priority": "HIGH",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Rapid Descent Rate Detected",
                    "detected": f"Aircraft vertical descent rate is {int(round(v_fpm)):,} ft/min.",
                    "why_it_matters": (
                        "Descent rate is elevated beyond standard stabilized approach guidelines (>1,000 fpm below 10,000 ft). "
                        "Requires monitoring for stabilized profile compliance."
                    ),
                    "triggering_data": f"Vertical rate: {int(round(v_fpm)):,} ft/min ({v_rate:.1f} m/s)",
                    "confidence": "High (ADS-B State Vector)",
                    "suggested_verification": "Verify target altitude, speed brakes configuration, and stabilization criteria.",
                }
            )
        elif v_fpm > 3800:
            alerts.append(
                {
                    "id": f"{icao24}_climb_med",
                    "priority": "MEDIUM",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Steep Climb Rate Detected",
                    "detected": f"Aircraft vertical climb rate is {int(round(v_fpm)):,} ft/min.",
                    "why_it_matters": (
                        "Climb rate is significantly elevated. Sustained steep climbs can erode airspeed margins "
                        "depending on aircraft weight and atmospheric conditions."
                    ),
                    "triggering_data": f"Vertical rate: {int(round(v_fpm)):,} ft/min ({v_rate:.1f} m/s)",
                    "confidence": "High (ADS-B State Vector)",
                    "suggested_verification": "Monitor indicated airspeed trend and engine thrust rating.",
                }
            )

    # ------------------------------------------------------------
    # 3. SPEED & ALTITUDE ENVELOPE CHECKS
    # ------------------------------------------------------------
    if not on_ground and alt_ft is not None and speed_kts is not None:
        # Low altitude high speed
        if alt_ft < 10000 and speed_kts > 285:
            alerts.append(
                {
                    "id": f"{icao24}_low_alt_speed",
                    "priority": "HIGH",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Low-Altitude High Speed Detected",
                    "detected": f"Aircraft speed is {int(round(speed_kts))} kts at {int(round(alt_ft)):,} ft.",
                    "why_it_matters": (
                        "Aviation regulations generally restrict speed below 10,000 ft MSL to 250 kts unless specific "
                        "ATC clearance is issued. High energy state increases pilot workload during descent/approach."
                    ),
                    "triggering_data": f"Ground speed: {int(round(speed_kts))} kts, Altitude: {int(round(alt_ft)):,} ft",
                    "confidence": "Medium (Ground speed proxy; wind correction may apply)",
                    "suggested_verification": "Cross-check tailwind component and ATC speed clearance.",
                }
            )

        # High altitude unusually low ground speed (possible stall margin or strong headwind)
        if alt_ft > 30000 and speed_kts < 155:
            alerts.append(
                {
                    "id": f"{icao24}_high_alt_slow",
                    "priority": "HIGH",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "High-Altitude Low Ground Speed Detected",
                    "detected": f"Aircraft speed is {int(round(speed_kts))} kts at Flight Level ~{int(round(alt_ft/100))}.",
                    "why_it_matters": (
                        "Unusually low ground speed at cruise altitude. Could indicate extreme jet stream headwinds "
                        "or low aerodynamic margin requiring attention."
                    ),
                    "triggering_data": f"Ground speed: {int(round(speed_kts))} kts, Altitude: {int(round(alt_ft)):,} ft",
                    "confidence": "Medium (Requires upper-air wind validation)",
                    "suggested_verification": "Review true airspeed vs ground speed and high-altitude winds aloft.",
                }
            )

    # ------------------------------------------------------------
    # 4. TELEMETRY UNCERTAINTY & SENSOR GAPS
    # ------------------------------------------------------------
    if not on_ground:
        if baro_alt is None and plane.get("geo_altitude") is None:
            alerts.append(
                {
                    "id": f"{icao24}_missing_alt",
                    "priority": "MEDIUM",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Missing Altitude Telemetry",
                    "detected": "Airborne state vector is missing barometric and geometric altitude readings.",
                    "why_it_matters": (
                        "Degraded situational awareness; vertical separation cannot be determined from received ADS-B packet alone."
                    ),
                    "triggering_data": "baro_altitude: None, geo_altitude: None",
                    "confidence": "High (Observed ADS-B Data Field)",
                    "suggested_verification": "Correlate with secondary radar data and flight plan estimates.",
                }
            )
        elif plane.get("heading") is None:
            alerts.append(
                {
                    "id": f"{icao24}_missing_heading",
                    "priority": "LOW",
                    "timestamp": now_str,
                    "callsign": callsign,
                    "icao24": icao24,
                    "alert_title": "Missing Track/Heading Vector",
                    "detected": "Aircraft trajectory vector missing true track or magnetic heading data.",
                    "why_it_matters": "Vector extrapolation uncertainty is elevated when heading is not broadcast.",
                    "triggering_data": "heading: None",
                    "confidence": "High (Observed ADS-B Data Field)",
                    "suggested_verification": "Derive direction from multi-point position history.",
                }
            )

    # ------------------------------------------------------------
    # 5. WEATHER PROXIMITY CORRELATION
    # ------------------------------------------------------------
    if weather_reports and lat is not None and lon is not None and not on_ground:
        for wx in weather_reports:
            w_lat = wx.get("latitude")
            w_lon = wx.get("longitude")
            if w_lat is None or w_lon is None:
                continue

            dist_km = calculate_distance_approx(lat, lon, w_lat, w_lon)

            # Within terminal area (~60 km) of station
            if dist_km <= 65.0:
                flt_cat = wx.get("flight_category", "VFR")
                wx_str = wx.get("weather_string", "")
                has_cb = wx.get("has_cumulonimbus", False)
                gust = wx.get("wind_gust_kt")

                if flt_cat == "LIFR" or "TS" in wx_str or has_cb:
                    alerts.append(
                        {
                            "id": f"{icao24}_wx_crit_{wx.get('icao')}",
                            "priority": "HIGH",
                            "timestamp": now_str,
                            "callsign": callsign,
                            "icao24": icao24,
                            "alert_title": f"Proximity to Severe Terminal Weather ({wx.get('icao')})",
                            "detected": (
                                f"Aircraft is within ~{int(round(dist_km))} km of {wx.get('icao')} "
                                f"reporting {flt_cat} conditions with {wx_str or 'convective clouds'}."
                            ),
                            "why_it_matters": (
                                "Convective activity, low ceiling, or thunderstorms in terminal vicinity substantially "
                                "elevate pilot workload, risk of go-around, turbulence, or diversion."
                            ),
                            "triggering_data": (
                                f"Station: {wx.get('icao')}, Category: {flt_cat}, Weather: {wx_str}, "
                                f"Distance: {int(round(dist_km))} km"
                            ),
                            "confidence": "Medium (Spatial proximity correlation)",
                            "suggested_verification": (
                                f"Check latest {wx.get('icao')} METAR/TAF, weather radar returns, and alternate aerodrome fuel."
                            ),
                        }
                    )
                    break  # Only one adverse weather proximity alert per aircraft
                elif flt_cat == "IFR" or (gust and gust >= 25):
                    alerts.append(
                        {
                            "id": f"{icao24}_wx_med_{wx.get('icao')}",
                            "priority": "MEDIUM",
                            "timestamp": now_str,
                            "callsign": callsign,
                            "icao24": icao24,
                            "alert_title": f"Adverse Weather Vicinity ({wx.get('icao')})",
                            "detected": (
                                f"Aircraft is within ~{int(round(dist_km))} km of {wx.get('icao')} "
                                f"reporting {flt_cat} (Wind: {wx.get('wind_speed_kt', 'N/A')} kt, Gust: {gust or 'None'} kt)."
                            ),
                            "why_it_matters": "Terminal weather may require instrument approach preparations and monitor of runway winds.",
                            "triggering_data": f"Station: {wx.get('icao')}, Distance: ~{int(round(dist_km))} km",
                            "confidence": "Medium (Spatial proximity correlation)",
                            "suggested_verification": f"Review destination {wx.get('icao')} ATIS and crosswind components.",
                        }
                    )
                    break

    return alerts


def evaluate_airspace_risks(
    aircraft_list: List[Dict[str, Any]],
    weather_reports: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """
    Evaluate entire monitored aircraft fleet against risk rules.
    Returns prioritized list of alerts sorted by severity (CRITICAL -> HIGH -> MEDIUM -> LOW).
    """
    all_alerts: List[Dict[str, Any]] = []

    for plane in aircraft_list:
        plane_alerts = evaluate_aircraft_risk(plane, weather_reports)
        all_alerts.extend(plane_alerts)

    # Sort alerts by severity rank
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_alerts.sort(key=lambda a: (severity_order.get(a["priority"], 99), a["callsign"]))

    return all_alerts
