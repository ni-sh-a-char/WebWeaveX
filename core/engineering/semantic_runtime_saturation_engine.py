from __future__ import annotations

from typing import Any, Dict


MAX_SATURATION = 100000


def measure_runtime_saturation(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    size = len(runtime_ir)
    return {
        "saturated": size >= MAX_SATURATION,
        "runtime_size": size,
    }
