"""
AeroGuardian AI - NOAA Aviation Weather Center Client

Retrieves and parses real METAR, TAF, and environmental condition data
from the official Aviation Weather Center Data API:
https://aviationweather.gov/api/data/

Strictly real aviation data only — handles missing fields gracefully as None / N/A.
"""

import time
from typing import Dict, Any, Optional, List, Tuple
import requests

AWC_BASE_URL = "https://aviationweather.gov/api/data"

# Standard presets for easy user exploration
POPULAR_AIRPORTS = {
    "VIDP": "Indira Gandhi Intl, Delhi (India)",
    "VOBL": "Kempegowda Intl, Bengaluru (India)",
    "VABB": "Chhatrapati Shivaji Intl, Mumbai (India)",
    "VOHS": "Rajiv Gandhi Intl, Hyderabad (India)",
    "VECC": "Netaji Subhash Chandra Bose Intl, Kolkata (India)",
    "VOMM": "Chennai Intl (India)",
    "VOCI": "Cochin Intl (India)",
    "VAAH": "Sardar Vallabhbhai Patel Intl, Ahmedabad (India)",
    "OMDB": "Dubai Intl (UAE)",
    "EGLL": "Heathrow Airport, London (UK)",
    "KJFK": "John F. Kennedy Intl, New York (USA)",
    "WSSS": "Singapore Changi Airport (Singapore)",
    "RJTT": "Haneda Airport, Tokyo (Japan)",
    "EDDF": "Frankfurt Airport (Germany)",
}

# In-memory cache for weather reports: {cache_key: (timestamp, data)}
_WEATHER_CACHE: Dict[str, Tuple[float, Any]] = {}
CACHE_TTL_SECONDS = 120.0  # Weather updates are typically issued every 30-60 mins

_STATUS: Dict[str, Any] = {
    "is_connected": False,
    "last_status": "Awaiting initial request",
    "last_fetch_time": 0.0,
    "monitored_stations": set(),
}


def _fetch_awc_endpoint(endpoint: str, icao: str, timeout: int = 12) -> Optional[List[Dict[str, Any]]]:
    """Internal helper to query AWC REST API in JSON format."""
    icao_clean = icao.strip().upper()
    cache_key = f"{endpoint}_{icao_clean}"
    now = time.time()

    if cache_key in _WEATHER_CACHE:
        cache_time, cached_val = _WEATHER_CACHE[cache_key]
        if now - cache_time < CACHE_TTL_SECONDS:
            return cached_val

    url = f"{AWC_BASE_URL}/{endpoint}"
    params = {"ids": icao_clean, "format": "json"}

    try:
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list):
            _WEATHER_CACHE[cache_key] = (now, data)
            _STATUS["is_connected"] = True
            _STATUS["last_status"] = "Connected"
            _STATUS["last_fetch_time"] = now
            _STATUS["monitored_stations"].add(icao_clean)
            return data
        return None
    except Exception as e:
        _STATUS["last_status"] = f"AWC API warning: {e}"
        # Check if we have stale cache to fall back on
        if cache_key in _WEATHER_CACHE:
            return _WEATHER_CACHE[cache_key][1]
        return None


def derive_flight_category(ceiling_ft: Optional[float], visibility_sm: Optional[float]) -> str:
    """
    Derive flight category based on FAA/ICAO standards:
    - LIFR: Ceiling < 500 ft and/or Visibility < 1 SM
    - IFR:  Ceiling 500 to <1,000 ft and/or Visibility 1 to <3 SM
    - MVFR: Ceiling 1,000 to 3,000 ft and/or Visibility 3 to 5 SM
    - VFR:  Ceiling > 3,000 ft and Visibility > 5 SM (or no ceiling)
    """
    if ceiling_ft is None and visibility_sm is None:
        return "UNKNOWN"

    c = ceiling_ft if ceiling_ft is not None else 99999
    v = visibility_sm if visibility_sm is not None else 999.0

    if c < 500 or v < 1.0:
        return "LIFR"
    elif c < 1000 or v < 3.0:
        return "IFR"
    elif c <= 3000 or v <= 5.0:
        return "MVFR"
    else:
        return "VFR"


def get_metar(icao: str) -> Optional[Dict[str, Any]]:
    """
    Fetch and decode real METAR for given ICAO station.
    Returns parsed dictionary or None if unavailable.
    """
    data = _fetch_awc_endpoint("metar", icao)
    if not data or len(data) == 0:
        return None

    raw_metar = data[0]

    # Calculate cloud ceiling (lowest broken or overcast layer)
    clouds = raw_metar.get("clouds") or []
    ceiling_ft = None
    has_cb = False
    for layer in clouds:
        cover = layer.get("cover", "")
        base = layer.get("base")
        c_type = layer.get("type", "")
        if c_type == "CB" or "CB" in str(layer):
            has_cb = True
        if cover in ("BKN", "OVC", "VV") and base is not None:
            if ceiling_ft is None or base < ceiling_ft:
                ceiling_ft = float(base)

    visib_sm = raw_metar.get("visib")
    try:
        visib_sm = float(visib_sm) if visib_sm is not None else None
    except (ValueError, TypeError):
        visib_sm = None

    # Flight category from API or derived
    flt_cat = raw_metar.get("fltCat") or derive_flight_category(ceiling_ft, visib_sm)

    # Dewpoint depression
    temp = raw_metar.get("temp")
    dewp = raw_metar.get("dewp")
    spread = None
    if temp is not None and dewp is not None:
        try:
            spread = round(float(temp) - float(dewp), 1)
        except (ValueError, TypeError):
            spread = None

    return {
        "icao": raw_metar.get("icaoId", icao.upper()),
        "name": raw_metar.get("name", "Unknown Airport"),
        "report_time": raw_metar.get("reportTime"),
        "raw_text": raw_metar.get("rawOb", "Raw observation unavailable"),
        "temperature_c": temp,
        "dewpoint_c": dewp,
        "temp_dewpoint_spread": spread,
        "wind_dir_deg": raw_metar.get("wdir"),
        "wind_speed_kt": raw_metar.get("wspd"),
        "wind_gust_kt": raw_metar.get("wgst"),
        "visibility_sm": visib_sm,
        "altimeter_hpa": raw_metar.get("altim"),
        "weather_string": raw_metar.get("wxString") or "None",
        "flight_category": flt_cat,
        "clouds": clouds,
        "ceiling_ft": ceiling_ft,
        "has_cumulonimbus": has_cb,
        "latitude": raw_metar.get("lat"),
        "longitude": raw_metar.get("lon"),
        "elevation_m": raw_metar.get("elev"),
    }


def get_taf(icao: str) -> Optional[Dict[str, Any]]:
    """
    Fetch and decode real Terminal Aerodrome Forecast (TAF).
    """
    data = _fetch_awc_endpoint("taf", icao)
    if not data or len(data) == 0:
        return None

    raw_taf = data[0]
    forecasts = raw_taf.get("fcsts") or []

    parsed_forecasts = []
    for fc in forecasts:
        parsed_forecasts.append(
            {
                "time_from": fc.get("timeFrom"),
                "time_to": fc.get("timeTo"),
                "change_type": fc.get("fcstChange") or "BASE",
                "wind_dir": fc.get("wdir"),
                "wind_speed_kt": fc.get("wspd"),
                "wind_gust_kt": fc.get("wgst"),
                "visibility_sm": fc.get("visib"),
                "weather_string": fc.get("wxString") or "None",
                "clouds": fc.get("clouds") or [],
            }
        )

    return {
        "icao": raw_taf.get("icaoId", icao.upper()),
        "name": raw_taf.get("name", "Unknown Station"),
        "issue_time": raw_taf.get("issueTime"),
        "raw_text": raw_taf.get("rawTAF", "Raw TAF unavailable"),
        "forecasts": parsed_forecasts,
    }


def get_weather_overview(icaos: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Fetch METAR for multiple stations to create an airspace weather snapshot.
    Defaults to major Indian commercial hub airports.
    """
    if icaos is None:
        icaos = ["VIDP", "VOBL", "VABB", "VOHS", "VECC", "VOMM"]

    reports = []
    for icao in icaos:
        metar = get_metar(icao)
        if metar:
            reports.append(metar)
    return reports


def get_weather_status() -> Dict[str, Any]:
    """Return status of weather data connectivity."""
    return {
        "is_connected": _STATUS["is_connected"],
        "status_text": _STATUS["last_status"],
        "stations_monitored_count": len(_STATUS["monitored_stations"]),
        "monitored_stations": list(_STATUS["monitored_stations"]),
        "last_fetch_time": _STATUS["last_fetch_time"],
    }
