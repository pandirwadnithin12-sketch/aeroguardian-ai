"""
SQLite storage for simulated alert history.

This database is local and educational. It does not connect to aircraft systems.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "aeroguardian.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the alerts table if it does not exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                flight_number TEXT,
                aircraft_id TEXT,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                sensor TEXT,
                sensor_value REAL,
                unit TEXT,
                recommendation TEXT,
                risk_score INTEGER
            )
            """
        )
        conn.commit()


def save_alert(
    alert_type: str,
    severity: str,
    sensor: str,
    sensor_value: float,
    unit: str,
    recommendation: str,
    flight_number: str = "AG-204",
    aircraft_id: str = "AG-772",
    risk_score: int = 0,
) -> None:
    """Insert one simulated alert row."""
    init_db()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO alerts (
                created_at, flight_number, aircraft_id, alert_type, severity,
                sensor, sensor_value, unit, recommendation, risk_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                flight_number,
                aircraft_id,
                alert_type,
                severity,
                sensor,
                float(sensor_value),
                unit,
                recommendation,
                int(risk_score),
            ),
        )
        conn.commit()


def save_analysis_alerts(analysis: dict) -> int:
    """Persist every grouped alert from an analysis result. Returns how many rows were written."""
    state = analysis["state"]
    actions = analysis.get("actions") or []
    rec_text = " | ".join(actions[:4]) if actions else "Review simulated indications."
    count = 0
    for alert in analysis.get("alerts") or []:
        save_alert(
            alert_type=alert["alert_type"],
            severity=alert["severity"],
            sensor=alert.get("sensor", ""),
            sensor_value=float(alert.get("value") or 0),
            unit=alert.get("unit") or "",
            recommendation=rec_text,
            flight_number=state.get("flight_number", "AG-204"),
            aircraft_id=state.get("aircraft_id", "AG-772"),
            risk_score=int(analysis.get("risk_score") or 0),
        )
        count += 1
    return count


def fetch_alerts(limit: int = 200) -> list[dict]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM alerts ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def alert_frequency() -> list[dict]:
    """Counts by alert type for the analytics page."""
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT alert_type, COUNT(*) AS count
            FROM alerts
            GROUP BY alert_type
            ORDER BY count DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def clear_alerts() -> None:
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM alerts")
        conn.commit()


def seed_demo_if_empty() -> None:
    """Add a few sample rows so first-time academic demos are not blank."""
    init_db()
    with get_connection() as conn:
        existing = conn.execute("SELECT COUNT(*) AS n FROM alerts").fetchone()["n"]
        if existing:
            return

    samples = [
        ("Engine Vibration", "HIGH", "engine_vibration", 78.0, "%", "Review simulated engine indications together."),
        ("Fuel Quantity", "MEDIUM", "fuel_level", 28.0, "%", "Monitor remaining simulated endurance."),
        ("Weather", "HIGH", "weather_severity", 8.0, "/10", "Discuss a simulated weather-avoidance option."),
        ("Cabin Pressure", "MEDIUM", "cabin_pressure", 82.0, "%", "Watch the simulated cabin-pressure trend."),
        ("Engine Health", "CRITICAL", "engine_combined", 121.0, "°C", "Prioritize combined engine-health review (academic only)."),
    ]
    for alert_type, severity, sensor, value, unit, rec in samples:
        save_alert(alert_type, severity, sensor, value, unit, rec, risk_score=55)
