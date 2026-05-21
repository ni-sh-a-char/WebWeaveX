from __future__ import annotations

import json
import math
import unicodedata
from typing import Any


def _norm_str(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _stable(value: Any, _depth: int = 0) -> Any:
    if _depth > 64:
        return str(value)
    if isinstance(value, str):
        return _norm_str(value)
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return 0.0
        return float(format(value, ".15g"))
    if isinstance(value, dict):
        return {
            _norm_str(str(k)): _stable(value[k], _depth + 1)
            for k in sorted(value.keys(), key=lambda x: _norm_str(str(x)))
        }
    if isinstance(value, (list, tuple)):
        items = [_stable(v, _depth + 1) for v in value]
        return sorted(
            items,
            key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        )
    return _norm_str(str(value))


def dumps_deterministic(value: Any) -> str:
    return json.dumps(_stable(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


dumps_canonical = dumps_deterministic
dumps_canonical_v4 = dumps_deterministic
dumps_canonical_v5 = dumps_deterministic
