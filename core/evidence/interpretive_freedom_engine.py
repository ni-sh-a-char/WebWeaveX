from __future__ import annotations

from typing import Any, Dict


def preserve_interpretive_freedom(autonomy: Dict[str, Any]) -> Dict[str, Any]:
    return {"free": autonomy.get("autonomous", True), "empire_blocked": True}
