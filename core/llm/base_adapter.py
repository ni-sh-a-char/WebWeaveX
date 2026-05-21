from __future__ import annotations

from typing import Dict


def disabled_result(provider: str, reason: str = "disabled") -> Dict[str, object]:
    return {"provider": provider, "enabled": False, "ok": False, "reason": reason, "output": ""}

