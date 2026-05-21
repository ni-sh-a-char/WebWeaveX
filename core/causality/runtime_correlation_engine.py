from __future__ import annotations

from typing import Any, Dict, List, Optional


def correlate_runtime_mutations(
    browser_events: Optional[List[Dict[str, Any]]] = None,
    native_events: Optional[List[Dict[str, Any]]] = None,
    notifications: Optional[List[Dict[str, Any]]] = None,
    terminal_lines: Optional[List[str]] = None,
    process_events: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    correlations: List[Dict[str, Any]] = []
    step = 0

    for event in list(browser_events or []):
        correlations.append({
            "kind": "ui_change",
            "event_id": str(event.get("id", f"browser:{step}")),
            "runtime": "browser",
            "step": step,
        })
        step += 1

    for line in list(terminal_lines or [])[:1000]:
        correlations.append({
            "kind": "terminal_log",
            "line": line,
            "runtime": "terminal",
            "step": step,
        })
        step += 1

    for notification in list(notifications or []):
        correlations.append({
            "kind": "notification",
            "payload": notification,
            "runtime": "desktop",
            "step": step,
        })
        step += 1

    for event in list(native_events or []):
        correlations.append({
            "kind": "native_mutation",
            "event_id": str(event.get("id", "")),
            "runtime": str(event.get("runtime", "desktop")),
            "step": step,
        })
        step += 1

    for proc in list(process_events or []):
        correlations.append({
            "kind": "process_mutation",
            "process": str(proc.get("name", "")),
            "runtime": "process",
            "step": step,
        })
        step += 1

    return {
        "correlations": sorted(correlations, key=lambda item: item["step"]),
        "count": len(correlations),
        "bounded": True,
    }
