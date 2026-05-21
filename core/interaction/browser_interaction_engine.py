from __future__ import annotations

from typing import Any, Dict, List, Optional

DEFAULT_TIMEOUT_MS = 30000
MAX_ACTIONS = 1000


def record_interaction(
    action: str,
    selector: str,
    metadata: Optional[Dict[str, Any]] = None,
    step: int = 0,
) -> Dict[str, Any]:
    return {
        "id": f"interaction_{step}",
        "timestamp": step,
        "action": str(action).strip(),
        "selector": str(selector).strip(),
        "metadata": dict(metadata or {}),
        "bounded": True,
    }


def build_interaction_plan(
    actions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    normalized: List[Dict[str, Any]] = []

    for index, action in enumerate(actions[:MAX_ACTIONS]):
        normalized.append(
            record_interaction(
                action=str(action.get("type", action.get("action", ""))),
                selector=str(action.get("selector", "")),
                metadata={
                    "value": action.get("value"),
                },
                step=index,
            )
        )

    return {
        "interaction_plan": normalized,
        "bounded": True,
    }


def _bounded_timeout(timeout_ms: Optional[int]) -> int:
    timeout = int(timeout_ms or DEFAULT_TIMEOUT_MS)
    return min(max(timeout, 1), DEFAULT_TIMEOUT_MS)


def click_element(
    page: Any,
    selector: str,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    timeout = _bounded_timeout(timeout_ms)

    if page is not None and hasattr(page, "click"):
        page.click(selector, timeout=timeout)

    return {
        "action": "click",
        "selector": selector,
        "timeout_ms": timeout,
        "bounded": True,
    }


def fill_input(
    page: Any,
    selector: str,
    value: str,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    timeout = _bounded_timeout(timeout_ms)

    if page is not None and hasattr(page, "fill"):
        page.fill(selector, str(value)[:5000], timeout=timeout)

    return {
        "action": "fill",
        "selector": selector,
        "value": str(value)[:5000],
        "timeout_ms": timeout,
        "bounded": True,
    }


def select_option(
    page: Any,
    selector: str,
    value: str,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    timeout = _bounded_timeout(timeout_ms)

    if page is not None and hasattr(page, "select_option"):
        page.select_option(selector, str(value)[:5000], timeout=timeout)

    return {
        "action": "select",
        "selector": selector,
        "value": str(value)[:5000],
        "timeout_ms": timeout,
        "bounded": True,
    }


def hover_element(
    page: Any,
    selector: str,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    timeout = _bounded_timeout(timeout_ms)

    if page is not None and hasattr(page, "hover"):
        page.hover(selector, timeout=timeout)

    return {
        "action": "hover",
        "selector": selector,
        "timeout_ms": timeout,
        "bounded": True,
    }


def wait_for_selector(
    page: Any,
    selector: str,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    timeout = _bounded_timeout(timeout_ms)

    if page is not None and hasattr(page, "wait_for_selector"):
        page.wait_for_selector(selector, timeout=timeout)

    return {
        "action": "wait",
        "selector": selector,
        "timeout_ms": timeout,
        "bounded": True,
    }
