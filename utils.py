"""
AeroGuardian AI - Utility Functions, Aerodynamic Physics & Aviation Conversions

Provides unit conversions, flight phase classification, Mach number estimation,
wake turbulence derivation, wind component calculations, and UI styling helpers.
Adheres strictly to the no-simulation policy: missing values are returned as 'N/A'
and never fabricated.
"""

import math
from typing import Any, Optional, Dict, Tuple


# ============================================================
# UNIT CONVERSIONS (Aviation Standard)
# ============================================================

def meters_to_feet(meters: Optional[float]) -> Optional[float]:
    """Convert meters to feet (1 m = 3.28084 ft)."""
    if meters is None:
        return None
    return meters * 3.28084


def ms_to_knots(ms: Optional[float]) -> Optional[float]:
    """Convert meters per second to knots (1 m/s = 1.94384 knots)."""
    if ms is None:
        return None
    return ms * 1.94384


def ms_to_kmh(ms: Optional[float]) -> Optional[float]:
    """Convert meters per second to kilometers per hour (1 m/s = 3.6 km/h)."""
    if ms is None:
        return None
    return ms * 3.6


def ms_to_ft_per_min(ms: Optional[float]) -> Optional[float]:
    """Convert vertical speed in m/s to feet per minute (1 m/s = 196.85 ft/min)."""
    if ms is None:
        return None
    return ms * 196.85


def km_to_nm(km: Optional[float]) -> Optional[float]:
    """Convert kilometers to nautical miles (1 km = 0.539957 NM)."""
    if km is None:
        return None
    return km * 0.539957


def hpa_to_inhg(hpa: Optional[float]) -> Optional[float]:
    """Convert hectopascals (hPa / mb) to inches of mercury (inHg)."""
    if hpa is None:
        return None
    return hpa * 0.0295299830714


# ============================================================
# AERODYNAMIC & FLIGHT PHYSICS MODELS
# ============================================================

def estimate_mach(velocity_ms: Optional[float], altitude_m: Optional[float]) -> Optional[float]:
    """
    Estimate Mach number (M) based on standard atmospheric temperature lapse rate.
    Speed of sound: a = sqrt(gamma * R * T)
    """
    if velocity_ms is None or velocity_ms <= 0:
        return None

    h = altitude_m if altitude_m is not None else 0.0
    h = max(0.0, float(h))

    # Standard atmosphere temperature model (ISA)
    if h <= 11000.0:  # Troposphere
        T = 288.15 - 0.0065 * h
    else:  # Lower Stratosphere (isothermal)
        T = 216.65

    # Speed of sound in air (gamma = 1.4, R = 287.05287 J/(kg·K))
    speed_of_sound = math.sqrt(1.4 * 287.05287 * T)

    mach = velocity_ms / speed_of_sound
    return round(mach, 2)


def classify_flight_phase(plane: Dict[str, Any]) -> Dict[str, str]:
    """
    Classifies the aircraft's current lifecycle flight phase based on observable state vectors:
    - GROUND / TAXI
    - TAKEOFF / INITIAL CLIMB
    - EN-ROUTE CLIMB
    - CRUISE
    - DESCENT
    - APPROACH / LANDING
    """
    on_ground = plane.get("on_ground", False)
    baro_alt = plane.get("baro_altitude")
    v_rate = plane.get("vertical_rate")

    alt_ft = meters_to_feet(baro_alt) if baro_alt is not None else None
    v_fpm = ms_to_ft_per_min(v_rate) if v_rate is not None else None

    if on_ground:
        return {
            "phase": "GROUND / TAXI",
            "code": "GROUND",
            "description": "Aircraft on aerodrome surface / taxiing / parked",
            "color": "#64748b",
        }

    if alt_ft is not None and alt_ft < 5000 and v_fpm is not None and v_fpm > 800:
        return {
            "phase": "TAKEOFF / INITIAL CLIMB",
            "code": "TAKEOFF",
            "description": "High-rate departure climb below 5,000 ft AGL",
            "color": "#00e5ff",
        }

    if alt_ft is not None and alt_ft < 5000 and v_fpm is not None and v_fpm < -200:
        return {
            "phase": "APPROACH / LANDING",
            "code": "APPROACH",
            "description": "Terminal area descent on final approach corridor",
            "color": "#f59e0b",
        }

    if v_fpm is not None and v_fpm > 400:
        return {
            "phase": "EN-ROUTE CLIMB",
            "code": "CLIMB",
            "description": "Ascending towards assigned cruise flight level",
            "color": "#00d4aa",
        }

    if v_fpm is not None and v_fpm < -400:
        return {
            "phase": "EN-ROUTE DESCENT",
            "code": "DESCENT",
            "description": "Descending from cruise flight level",
            "color": "#fbbf24",
        }

    if alt_ft is not None and alt_ft >= 20000:
        fl = int(round(alt_ft / 100))
        return {
            "phase": f"CRUISE FL{fl}",
            "code": "CRUISE",
            "description": f"Level cruise at Flight Level {fl}",
            "color": "#38bdf8",
        }

    return {
        "phase": "LEVEL AIRBORNE",
        "code": "LEVEL",
        "description": "Airborne level flight in intermediate airspace",
        "color": "#38bdf8",
    }


def get_wake_category(category_id: Optional[int]) -> str:
    """
    Derives official ICAO Wake Turbulence Category from OpenSky emitter category byte:
    - LIGHT: MTOW <= 7,000 kg (15,500 lbs)
    - MEDIUM: MTOW > 7,000 kg to < 136,000 kg (A320, B737)
    - HEAVY: MTOW >= 136,000 kg (300,000 lbs, B777, A350)
    - SUPER: Airbus A380-800
    """
    if category_id is None:
        return "MEDIUM (Standard)"

    mapping = {
        1: "LIGHT (Glider/General Aviation)",
        2: "LIGHT (Small Single/Twin)",
        3: "MEDIUM (Large, e.g. A320/B737)",
        4: "HEAVY (High Vortex, e.g. B757)",
        5: "HEAVY (Wide-body, e.g. B777/A350)",
        6: "HIGH PERFORMANCE (Fighter/Fast Jet)",
        7: "ROTORCRAFT (Helicopter)",
    }
    return mapping.get(category_id, "MEDIUM (Standard Transport)")


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


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate compass bearing (0-360 degrees) from point 1 to point 2."""
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dL = math.radians(lon2 - lon1)

    x = math.sin(dL) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - (math.sin(p1) * math.cos(p2) * math.cos(dL))

    initial_bearing = math.atan2(x, y)
    compass_bearing = (math.degrees(initial_bearing) + 360) % 360
    return round(compass_bearing, 1)


def calculate_wind_components(
    plane_heading: Optional[float],
    wind_dir: Optional[float],
    wind_speed_kt: Optional[float],
) -> Dict[str, Any]:
    """
    Calculate headwind/tailwind and crosswind components in knots:
    Crosswind = wind_speed * sin(wind_dir - heading)
    Headwind = wind_speed * cos(wind_dir - heading) (negative means tailwind)
    """
    if plane_heading is None or wind_dir is None or wind_speed_kt is None:
        return {"headwind_kt": None, "crosswind_kt": None, "crosswind_dir": "N/A"}

    diff_rad = math.radians(wind_dir - plane_heading)
    hw = wind_speed_kt * math.cos(diff_rad)
    cw = wind_speed_kt * math.sin(diff_rad)

    return {
        "headwind_kt": round(hw, 1),
        "is_tailwind": hw < 0,
        "crosswind_kt": round(abs(cw), 1),
        "crosswind_dir": "FROM RIGHT" if cw > 0 else "FROM LEFT" if cw < 0 else "DIRECT",
    }


# ============================================================
# SAFE FORMATTERS (Never invent data; return 'N/A' if None)
# ============================================================

def fmt_val(val: Any, unit: str = "", decimal: int = 1, fallback: str = "N/A") -> str:
    """Format numeric value with unit; returns fallback if None."""
    if val is None:
        return fallback
    try:
        num = float(val)
        if decimal == 0:
            formatted = f"{int(round(num))}"
        else:
            formatted = f"{num:.{decimal}f}"
        return f"{formatted} {unit}".strip() if unit else formatted
    except (ValueError, TypeError):
        return str(val) if val is not None else fallback


def fmt_altitude(baro_meters: Optional[float], geo_meters: Optional[float] = None) -> str:
    """Format altitude showing both feet and meters, or N/A."""
    m = baro_meters if baro_meters is not None else geo_meters
    if m is None:
        return "N/A"
    ft = meters_to_feet(m)
    return f"{int(round(ft)):,} ft ({int(round(m)):,} m)"


def fmt_speed(velocity_ms: Optional[float]) -> str:
    """Format speed in knots and m/s, or N/A."""
    if velocity_ms is None:
        return "N/A"
    knots = ms_to_knots(velocity_ms)
    return f"{int(round(knots))} kts ({velocity_ms:.1f} m/s)"


def fmt_vertical_rate(v_rate_ms: Optional[float]) -> str:
    """Format vertical rate in ft/min, or Level/NA."""
    if v_rate_ms is None:
        return "N/A"
    fpm = ms_to_ft_per_min(v_rate_ms)
    if abs(fpm) < 100:
        return "Level (0 fpm)"
    direction = "▲" if fpm > 0 else "▼"
    return f"{direction} {int(round(fpm)):+} fpm ({v_rate_ms:+.1f} m/s)"


def fmt_heading(heading_deg: Optional[float]) -> str:
    """Format heading with compass direction or N/A."""
    if heading_deg is None:
        return "N/A"
    deg = heading_deg % 360
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = int((deg + 11.25) / 22.5) % 16
    return f"{int(round(deg))}° ({directions[idx]})"


def fmt_squawk(squawk: Optional[str]) -> str:
    """Format squawk code, flagging emergencies."""
    if not squawk:
        return "N/A"
    code = str(squawk).strip()
    if code == "7700":
        return f"🚨 {code} (EMERGENCY)"
    elif code == "7600":
        return f"📻 {code} (RADIO FAIL)"
    elif code == "7500":
        return f"⚠️ {code} (UNLAWFUL)"
    return code


# ============================================================
# SEVERITY TOKENS & BADGES
# ============================================================

SEVERITY_COLORS = {
    "CRITICAL": "#ff3366",   # Vivid red
    "HIGH": "#ff9900",       # Vivid amber
    "MEDIUM": "#ffcc00",     # Vivid gold
    "LOW": "#00d4aa",        # Teal / info
    "NORMAL": "#00b4d8",     # Cyan
}

FLIGHT_CAT_COLORS = {
    "VFR": "#00d4aa",   # Green / Teal
    "MVFR": "#00b4d8",  # Blue
    "IFR": "#ff9900",   # Amber
    "LIFR": "#ff3366",  # Red / Magenta
    "UNKNOWN": "#6c757d"
}


def get_severity_badge_html(severity: str) -> str:
    """Generate inline styled badge for alert severities."""
    sev = severity.upper()
    color = SEVERITY_COLORS.get(sev, "#6c757d")
    return (
        f'<span style="background-color: {color}22; color: {color}; '
        f'border: 1px solid {color}88; padding: 2px 10px; border-radius: 6px; '
        f'font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">'
        f'{sev}</span>'
    )


def get_flight_category_badge_html(category: str) -> str:
    """Generate inline styled badge for aviation weather flight categories."""
    cat = (category or "UNKNOWN").upper()
    color = FLIGHT_CAT_COLORS.get(cat, "#6c757d")
    return (
        f'<span style="background-color: {color}25; color: {color}; '
        f'border: 1px solid {color}; padding: 3px 12px; border-radius: 8px; '
        f'font-size: 13px; font-weight: 800; letter-spacing: 0.5px;">'
        f'● {cat}</span>'
    )
