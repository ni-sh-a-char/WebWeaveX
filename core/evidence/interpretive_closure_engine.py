from __future__ import annotations

from typing import Any, Dict


def detect_interpretive_closure(plurality_count: int, depth: int) -> Dict[str, Any]:
    closed = plurality_count < 2 and depth >= 2
    return {"closure_detected": closed, "suppress": closed, "closure_pressure": {"level": 0.75 if closed else 0.0}}
