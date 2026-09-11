"""
AeroGuardian AI - Intelligent Alert Management System

Handles alert prioritization, deduplication, state tracking,
acknowledgment, and history filtering.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class AlertManager:
    """Manages alert lifecycle, prioritization, and acknowledgment states."""

    def __init__(self):
        # Key: alert_id, Value: alert dict
        self._alerts: Dict[str, Dict[str, Any]] = {}
        self._acknowledged_ids: set = set()
        self._history: List[Dict[str, Any]] = []

    def sync_alerts(self, new_alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge newly evaluated alerts with current state.
        Preserves acknowledgment status and tracks active vs cleared alerts.
        """
        active_ids = set()

        for alert in new_alerts:
            aid = alert["id"]
            active_ids.add(aid)

            is_ack = aid in self._acknowledged_ids
            alert_copy = dict(alert)
            alert_copy["acknowledged"] = is_ack

            if aid not in self._alerts:
                # Newly raised alert
                self._alerts[aid] = alert_copy
                self._history.append(alert_copy)
            else:
                # Update existing alert with latest telemetry triggering data
                self._alerts[aid]["triggering_data"] = alert_copy["triggering_data"]
                self._alerts[aid]["timestamp"] = alert_copy["timestamp"]
                self._alerts[aid]["acknowledged"] = is_ack

        # Mark or prune alerts that are no longer active
        keys_to_remove = [k for k in self._alerts if k not in active_ids]
        for k in keys_to_remove:
            # Keep in history, remove from active registry
            del self._alerts[k]

        return self.get_active_alerts()

    def get_active_alerts(
        self,
        priority_filter: Optional[str] = None,
        include_acknowledged: bool = True,
        search_query: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return active alerts sorted by severity and filtered by criteria."""
        severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        alerts = list(self._alerts.values())

        if priority_filter and priority_filter.upper() != "ALL":
            alerts = [a for a in alerts if a["priority"].upper() == priority_filter.upper()]

        if not include_acknowledged:
            alerts = [a for a in alerts if not a.get("acknowledged", False)]

        if search_query:
            q = search_query.strip().lower()
            alerts = [
                a for a in alerts
                if q in a.get("callsign", "").lower()
                or q in a.get("icao24", "").lower()
                or q in a.get("alert_title", "").lower()
                or q in a.get("detected", "").lower()
            ]

        alerts.sort(key=lambda x: (severity_rank.get(x["priority"], 99), x.get("timestamp", "")))
        return alerts

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Mark an alert as acknowledged by the operator."""
        self._acknowledged_ids.add(alert_id)
        if alert_id in self._alerts:
            self._alerts[alert_id]["acknowledged"] = True
            return True
        return False

    def unacknowledge_alert(self, alert_id: str) -> bool:
        """Unmark an acknowledged alert."""
        if alert_id in self._acknowledged_ids:
            self._acknowledged_ids.remove(alert_id)
        if alert_id in self._alerts:
            self._alerts[alert_id]["acknowledged"] = False
            return True
        return False

    def clear_acknowledged(self):
        """Remove acknowledged alerts from active display."""
        to_del = [aid for aid, a in self._alerts.items() if a.get("acknowledged", False)]
        for aid in to_del:
            del self._alerts[aid]

    def get_severity_counts(self) -> Dict[str, int]:
        """Return counts of active alerts grouped by priority."""
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for a in self._alerts.values():
            pri = a.get("priority", "LOW").upper()
            if pri in counts:
                counts[pri] += 1
            else:
                counts[pri] = 1
        return counts

    def get_history(self) -> List[Dict[str, Any]]:
        """Return chronological record of all alerts detected in this session."""
        return list(reversed(self._history))
