from __future__ import annotations

from typing import Any, Dict, List

OBJECTIVES = {
    "login": ["open_login", "fill_credentials", "submit"],
    "extract_dashboard": ["navigate_dashboard", "capture_widgets", "capture_tables"],
    "export_report": ["open_reports", "select_report", "export"],
    "extract_invoices": ["open_invoices", "paginate", "extract_rows"],
    "monitor_metrics": ["open_dashboard", "observe_metrics", "checkpoint"],
}


def build_runtime_goal(objective: str) -> Dict[str, Any]:
    steps = OBJECTIVES.get(objective, ["observe", "extract"])

    return {
        "objective": objective,
        "steps": list(steps),
        "bounded": True,
    }
