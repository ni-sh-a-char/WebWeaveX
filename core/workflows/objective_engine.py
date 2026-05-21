from __future__ import annotations

from typing import Any, Dict, List


OBJECTIVE_STEPS: Dict[str, List[str]] = {
    "extract_dashboard": ["navigate_dashboard", "capture_widgets", "capture_tables"],
    "extract_invoices": ["open_invoices", "paginate", "extract_rows"],
    "monitor_metrics": ["open_dashboard", "observe_metrics", "checkpoint"],
    "capture_notifications": ["observe_notifications", "capture_events", "checkpoint"],
    "extract_repository": ["scan_repository", "extract_structure", "compile_graph"],
    "monitor_runtime": ["observe_runtime", "capture_mutations", "checkpoint"],
    "capture_terminal": ["open_terminal", "capture_output", "checkpoint"],
    "monitor_application": ["observe_application", "capture_state", "checkpoint"],
    "extract_api_surface": ["discover_routes", "extract_endpoints", "compile_api"],
    "monitor_infrastructure": ["observe_infra", "capture_status", "checkpoint"],
}


def build_runtime_objective(
    objective: str,
    priority: int = 0,
) -> Dict[str, Any]:
    steps = list(OBJECTIVE_STEPS.get(objective, ["observe", "extract", "checkpoint"]))

    return {
        "objective": objective,
        "priority": priority,
        "steps": steps,
        "bounded": True,
    }
