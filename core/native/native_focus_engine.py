from __future__ import annotations

from typing import Any, Dict


def resolve_native_focus(
    windows: Dict[str, Any],
    accessibility: Dict[str, Any],
) -> Dict[str, Any]:
    focused_window = str(windows.get("focused_window", ""))

    focused_control = {}
    for bucket in ("buttons", "text_inputs", "tabs"):
        for element in accessibility.get(bucket, []):
            if element.get("focused"):
                focused_control = element
                break
        if focused_control:
            break

    return {
        "window": focused_window,
        "control": focused_control,
        "bounded": True,
    }
