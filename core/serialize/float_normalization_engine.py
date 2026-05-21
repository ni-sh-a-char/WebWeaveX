from __future__ import annotations

import math


def normalize_float(value: float) -> float:
    if math.isnan(value) or math.isinf(value):
        return 0.0
    return float(format(value, ".15g"))
