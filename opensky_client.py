"""
AeroGuardian AI - OpenSky Network Client

Fetches real aircraft state vectors directly from the OpenSky Network API.
Strictly adheres to the no-simulation policy: real data only, missing fields
are set to None (displayed as 'N/A' in UI). Never generates fake aircraft.

API Docs: https://opensky-network.org/apidoc/rest.html
"""

import os
import time
from typing import List, Dict, Any, Optional, Tuple
import requests
from dotenv import load_dotenv

load_dotenv()

OPENSKY_URL = "https://opensky-network.org/api/states/all"

# Bounding box presets (lamin, lomin, lamax, lomax)
REGION_BOUNDS: Dict[str, Optional[Tuple[float, float, float, float]]] = {
    "India": (8.0, 68.0, 37.0, 97.0),
    "Global": None,
    "Europe": (35.0, -10.0, 70.0, 40.0),
    "North America": (24.0, -125.0, 50.0, -66.0),
    "Southeast Asia": (-10.0, 95.0, 20.0, 141.0),
    "Middle East": (12.0, 34.0, 38.0, 63.0),
}

# Cache to avoid aggressive polling and OpenSky 429 rate limit errors
_CACHE: Dict[str, Any] = {
    "data": [],
    "last_fetched": 0.0,
    "last_region": None,
    "last_status": "Not connected yet",
    "is_connected": False,
    "error_message": None,
}

CACHE_TTL_SECONDS = 12.0  # OpenSky anonymous rate limit is ~10s per request


def get_opensky_auth() -> Optional[Tuple[str, str]]:
    """Retrieve OpenSky basic auth credentials if configured in environment."""
    user = os.getenv("OPENSKY_USERNAME") or os.getenv("OPENSKY_CLIENT_ID")
    pwd = os.getenv("OPENSKY_PASSWORD") or os.getenv("OPENSKY_CLIENT_SECRET")
    if user and pwd and "your_" not in user.lower() and "your_" not in pwd.lower():
        return (user, pwd)
    return None


def get_live_aircraft(
    lamin: Optional[float] = 8.0,
    lomin: Optional[float] = 68.0,
    lamax: Optional[float] = 37.0,
    lomax: Optional[float] = 97.0,
    force_refresh: bool = False,
    timeout: int = 15,
) -> List[Dict[str, Any]]:
    """
    Fetch real-time aircraft state data from OpenSky Network.
    Default bounding box covers the Indian subcontinent.
    If all coordinates are None, queries worldwide state vectors.
    """
    global _CACHE

    current_time = time.time()
    cache_key = f"{lamin}_{lomin}_{lamax}_{lomax}"

    # Return cached data if within TTL and not forcing refresh
    if (
        not force_refresh
        and _CACHE["last_region"] == cache_key
        and (current_time - _CACHE["last_fetched"]) < CACHE_TTL_SECONDS
        and _CACHE["data"]
    ):
        return _CACHE["data"]

    params: Dict[str, float] = {}
    if lamin is not None and lomin is not None and lamax is not None and lomax is not None:
        params = {
            "lamin": float(lamin),
            "lomin": float(lomin),
            "lamax": float(lamax),
            "lomax": float(lomax),
        }

    auth = get_opensky_auth()

    try:
        response = requests.get(
            OPENSKY_URL,
            params=params if params else None,
            auth=auth,
            timeout=timeout,
        )

        if response.status_code == 429:
            # OpenSky rate limit reached. Fallback to open live ADS-B network
            print("[INFO] OpenSky rate-limited (HTTP 429). Ingesting live open ADS-B network stream...")
            fallback_planes = fetch_open_adsb_live(lamin, lomin, lamax, lomax)
            if fallback_planes:
                _CACHE["data"] = fallback_planes
                _CACHE["last_fetched"] = current_time
                _CACHE["last_region"] = cache_key
                _CACHE["last_status"] = f"Connected via Open ADS-B Network ({len(fallback_planes)} live aircraft received)"
                _CACHE["is_connected"] = True
                _CACHE["error_message"] = None
                return fallback_planes

            _CACHE["last_status"] = "Rate limit reached (HTTP 429). Returning cached state."
            _CACHE["error_message"] = "OpenSky rate limit reached. Please wait a few seconds before refreshing."
            if _CACHE["data"]:
                return _CACHE["data"]
            raise RuntimeError("OpenSky API rate limit reached (HTTP 429). Please wait 15 seconds.")

        response.raise_for_status()

        data = response.json()
        states = data.get("states") or []

        aircraft_list: List[Dict[str, Any]] = []

        for row in states:
            # OpenSky state vector mapping according to official REST API:
            # 0: icao24, 1: callsign, 2: origin_country, 3: time_position, 4: last_contact,
            # 5: longitude, 6: latitude, 7: baro_altitude, 8: on_ground, 9: velocity,
            # 10: true_track, 11: vertical_rate, 12: sensors, 13: geo_altitude,
            # 14: squawk, 15: spi, 16: position_source, 17: category
            aircraft_list.append(
                {
                    "icao24": str(row[0]) if row[0] else "N/A",
                    "callsign": (row[1] or "").strip() or "N/A",
                    "country": row[2] or "Unknown",
                    "time_position": row[3],
                    "last_contact": row[4],
                    "longitude": row[5] if row[5] is not None else None,
                    "latitude": row[6] if row[6] is not None else None,
                    "baro_altitude": row[7] if row[7] is not None else None,
                    "on_ground": bool(row[8]) if row[8] is not None else False,
                    "velocity": row[9] if row[9] is not None else None,
                    "heading": row[10] if row[10] is not None else None,
                    "vertical_rate": row[11] if row[11] is not None else None,
                    "geo_altitude": row[13] if len(row) > 13 and row[13] is not None else None,
                    "squawk": str(row[14]).strip() if len(row) > 14 and row[14] else None,
                    "category": row[17] if len(row) > 17 else None,
                }
            )

        _CACHE["data"] = aircraft_list
        _CACHE["last_fetched"] = current_time
        _CACHE["last_region"] = cache_key
        _CACHE["last_status"] = f"Connected ({len(aircraft_list)} aircraft received)"
        _CACHE["is_connected"] = True
        _CACHE["error_message"] = None

        return aircraft_list

    except Exception as exc:
        # Try open ADS-B network as fallback if exception occurred
        fallback_planes = fetch_open_adsb_live(lamin, lomin, lamax, lomax)
        if fallback_planes:
            _CACHE["data"] = fallback_planes
            _CACHE["last_fetched"] = current_time
            _CACHE["last_region"] = cache_key
            _CACHE["last_status"] = f"Connected via Open ADS-B Network ({len(fallback_planes)} live aircraft received)"
            _CACHE["is_connected"] = True
            _CACHE["error_message"] = None
            return fallback_planes

        _CACHE["is_connected"] = False
        _CACHE["error_message"] = str(exc)
        _CACHE["last_status"] = f"Connection error: {exc}"
        if _CACHE["data"]:
            return _CACHE["data"]
        raise exc


def fetch_open_adsb_live(
    lamin: Optional[float] = None,
    lomin: Optional[float] = None,
    lamax: Optional[float] = None,
    lomax: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Ingest real live ADS-B state vectors from the open ADS-B receiver network.
    Automatically engaged if OpenSky anonymous daily quota hits HTTP 429.
    Provides 100% genuine live aircraft telemetry without simulation.
    """
    if lamin is not None and lamax is not None and lomin is not None and lomax is not None:
        lat_c = round((float(lamin) + float(lamax)) / 2.0, 3)
        lon_c = round((float(lomin) + float(lomax)) / 2.0, 3)
        radius = 750
    else:
        lat_c, lon_c, radius = 50.0, 10.0, 800

    url = f"https://api.adsb.lol/v2/point/{lat_c}/{lon_c}/{radius}"
    headers = {"User-Agent": "AeroGuardian-Research/2.0 (OpenADS-B Ingestion)"}

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code != 200:
            return []

        data = resp.json()
        ac_list = data.get("ac") or []
        parsed = []
        now = time.time()

        for ac in ac_list:
            lat = ac.get("lat")
            lon = ac.get("lon")
            if lat is None or lon is None:
                continue

            alt_baro = ac.get("alt_baro")
            is_ground = alt_baro == "ground" or ac.get("ground", False)
            alt_m = float(alt_baro) * 0.3048 if isinstance(alt_baro, (int, float)) else (0.0 if is_ground else None)

            gs_kts = ac.get("gs")
            vel_ms = float(gs_kts) * 0.514444 if isinstance(gs_kts, (int, float)) else None

            vr_fpm = ac.get("baro_rate")
            vr_ms = float(vr_fpm) * 0.00508 if isinstance(vr_fpm, (int, float)) else None

            geo_alt = ac.get("alt_geom")
            geo_m = float(geo_alt) * 0.3048 if isinstance(geo_alt, (int, float)) else None

            heading = ac.get("true_heading") if ac.get("true_heading") is not None else ac.get("track")

            r = str(ac.get("r") or "").upper()
            country = "Unknown"
            if r.startswith("VT-"): country = "India"
            elif r.startswith("N"): country = "United States"
            elif r.startswith("G-"): country = "United Kingdom"
            elif r.startswith("F-"): country = "France"
            elif r.startswith("D-"): country = "Germany"
            elif r.startswith("A6-"): country = "United Arab Emirates"
            elif r.startswith("9V-"): country = "Singapore"
            elif r.startswith("B-"): country = "China"
            elif r.startswith("JA"): country = "Japan"
            elif r.startswith("VH-"): country = "Australia"
            elif r.startswith("9M-"): country = "Malaysia"
            elif r.startswith("HS-"): country = "Thailand"
            elif r.startswith("AP-"): country = "Pakistan"
            elif r.startswith("4R-"): country = "Sri Lanka"
            elif r.startswith("TC-"): country = "Turkey"
            elif r.startswith("C-"): country = "Canada"

            cat_raw = ac.get("category")
            cat_val = None
            if isinstance(cat_raw, str) and len(cat_raw) >= 2 and cat_raw[1].isdigit():
                cat_val = int(cat_raw[1])
            elif isinstance(cat_raw, int):
                cat_val = cat_raw

            parsed.append({
                "icao24": str(ac.get("hex") or "").lower(),
                "callsign": (ac.get("flight") or "").strip() or "N/A",
                "country": country,
                "time_position": int(now - ac.get("seen_pos", 0)),
                "last_contact": int(now - ac.get("seen", 0)),
                "longitude": lon,
                "latitude": lat,
                "baro_altitude": alt_m,
                "on_ground": is_ground,
                "velocity": vel_ms,
                "heading": heading,
                "vertical_rate": vr_ms,
                "geo_altitude": geo_m,
                "squawk": str(ac.get("squawk") or "").strip() or None,
                "category": cat_val,
                "mach": ac.get("mach"),
                "aircraft_type": ac.get("t"),
                "registration": ac.get("r"),
            })

        return parsed
    except Exception as e:
        print(f"[WARN] Open ADS-B query error: {e}")
        return []


def get_live_aircraft_by_region(
    region_name: str = "India",
    force_refresh: bool = False,
) -> List[Dict[str, Any]]:
    """Helper to fetch live aircraft using region preset name."""
    bounds = REGION_BOUNDS.get(region_name, REGION_BOUNDS["India"])
    if bounds is None:
        return get_live_aircraft(None, None, None, None, force_refresh=force_refresh)
    return get_live_aircraft(
        lamin=bounds[0],
        lomin=bounds[1],
        lamax=bounds[2],
        lomax=bounds[3],
        force_refresh=force_refresh,
    )


def get_opensky_status() -> Dict[str, Any]:
    """Return current connection and cache status."""
    return {
        "is_connected": _CACHE["is_connected"],
        "status_text": _CACHE["last_status"],
        "last_fetched": _CACHE["last_fetched"],
        "count": len(_CACHE["data"]),
        "error_message": _CACHE["error_message"],
    }