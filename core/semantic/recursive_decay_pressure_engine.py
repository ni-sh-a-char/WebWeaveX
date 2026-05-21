from __future__ import annotations

from typing import Any, Dict


def compute_recursive_decay_pressure(depth: int) -> Dict[str, Any]:
    return {"pressure": round(min(1.0, depth * 0.1), 3), "depth": depth}
