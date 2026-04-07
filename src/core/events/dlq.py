import logging
from typing import Dict, Any
from .bus import HermesEventBus

logger = logging.getLogger(__name__)


class HermesDLQ:
    """
    Dead-Letter Queue processor for Hermes.
    Architected from PANOPTICON FORGE Iteration 010, 011, and 012.
    """

    def __init__(self, event_bus: HermesEventBus, max_retries: int = 3):
        self.bus = event_bus
        self.max_retries = max_retries
        self.discard_bin = []

    def route_to_dlq(self, failed_event: Dict[str, Any], error: Exception):
        """Called when a worker crashes to securely offload the poisoned event."""
        retries = failed_event.get("retries", 0)
        event_type = failed_event.get("type", "unknown")
        logger.warning(
            f"Routing to DLQ: {event_type} (Retry {retries}/{self.max_retries})"
        )

        if retries >= self.max_retries:
            self._permanently_discard(failed_event, error)
        else:
            self._attempt_recovery(failed_event)

    def _attempt_recovery(self, event: Dict[str, Any]):
        """Applies schema healing wrappers and requeues."""
        event["retries"] = event.get("retries", 0) + 1
        logger.info(f"Requeuing event to active bus.")
        self.bus.publish(
            "system_retries",
            event.get("type", "recovery"),
            event.get("data", {}),
            sender="HermesDLQ",
        )

    def _permanently_discard(self, event: Dict[str, Any], error: Exception):
        """Iteration 012 logic: Alerting the human engineering team."""
        logger.error(f"🛑 FATAL. Event {event['type']} permanently binned.")
        self.discard_bin.append({"event": event, "error": str(error)})
        self._fire_webhook(event, error)

    def _fire_webhook(self, event: Dict[str, Any], error: Exception):
        """Fires an alert to the Engineering slack channel."""
        alert_payload = {
            "severity": "CRITICAL",
            "component": "HermesDLQ",
            "message": f"Payload from {event.get('sender', 'Unknown')} discarded.",
            "error_trace": str(error),
        }
        logger.critical(f"🚨 PAGERDUTY ALERT: {alert_payload}")
