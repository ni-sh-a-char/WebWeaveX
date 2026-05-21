from __future__ import annotations

from typing import Any, Dict, List, Optional


def reconstruct_browser_runtime(
    browser_ir: Optional[Dict[str, Any]] = None,
    interaction_ir: Optional[Dict[str, Any]] = None,
    identity: Optional[Dict[str, Any]] = None,
    session: Optional[Dict[str, Any]] = None,
    streaming: Optional[Dict[str, Any]] = None,
    dom: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    browser_ir = browser_ir or {}
    interaction_ir = interaction_ir or {}
    identity = identity or {}
    session = session or {}
    streaming = streaming or {}
    dom = dom or {}

    tabs = sorted(
        [
            {"id": f"tab:{index}", "path": str(route.get("path", ""))}
            for index, route in enumerate(
                interaction_ir.get("tab_states", {}).get("tabs", [])
                or browser_ir.get("routes", {}).get("history", [])
                or [{"path": browser_ir.get("url", "/")}]
            )
        ],
        key=lambda item: item["id"],
    )

    navigation_history = sorted(
        [
            {"path": str(item.get("path", "")), "order": int(item.get("order", index))}
            for index, item in enumerate(
                interaction_ir.get("route_transitions", {}).get("routes", [])
                or browser_ir.get("navigation", {}).get("history", [])
                or []
            )
        ],
        key=lambda item: item["order"],
    )

    return {
        "tabs": tabs,
        "navigation_history": navigation_history,
        "dom_structure": dict(dom.get("structure", dom.get("nodes", {}))),
        "interaction_flows": list(interaction_ir.get("interactions", []))[:1000],
        "browser_identity": dict(identity),
        "authenticated_state": {
            "authenticated": bool(session.get("authenticated", False)),
            "cookies": sorted(session.get("cookies", []), key=lambda c: str(c.get("name", ""))),
        },
        "storage": {
            "local": dict(session.get("local_storage", {})),
            "session": dict(session.get("session_storage", {})),
        },
        "streaming_state": dict(streaming),
        "replay_safe": True,
        "bounded": True,
    }
