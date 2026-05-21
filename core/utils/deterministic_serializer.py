from __future__ import annotations

import json
import unicodedata
from typing import Any


def _norm_str(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _stable(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _stable(value[k]) for k in sorted(value.keys(), key=lambda x: _norm_str(str(x)))}
    if isinstance(value, list):
        normalized = [_stable(v) for v in value]
        return sorted(normalized, key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    if isinstance(value, str):
        return _norm_str(value)
    return value


def dumps_deterministic(value: Any) -> str:
    return json.dumps(_stable(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
