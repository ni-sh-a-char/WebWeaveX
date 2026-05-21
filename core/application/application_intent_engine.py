from __future__ import annotations

from typing import Any, Dict


INTENT_MAP = {
    "extract_dashboard": "observe_metrics",
    "login": "authenticate",
    "export_report": "export_data",
    "extract_invoices": "collect_records",
    "monitor_metrics": "continuous_observe",
}


def resolve_application_intent(objective: str) -> Dict[str, Any]:
    return {
        "objective": objective,
        "intent": INTENT_MAP.get(objective, "observe"),
        "bounded": True,
    }
