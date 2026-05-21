from __future__ import annotations

from typing import Any, Dict, Optional


def align_native_runtime(
    native_state: Dict[str, Any],
    adaptive_runtime: Optional[Dict[str, Any]] = None,
    application_memory: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    adaptive_runtime = adaptive_runtime or {}
    application_memory = application_memory or {}

    return {
        "native_runtime": native_state.get("runtime", ""),
        "adaptive_healed": list(adaptive_runtime.get("healed_selectors", []))[:1000],
        "application_objectives": list(
            application_memory.get("objectives", [])
        ),
        "aligned": True,
        "bounded": True,
    }
