from __future__ import annotations

from typing import Any, Dict


def apply_worldview_antigravity(convergence_suppressed: bool) -> Dict[str, Any]:
    return {"active": True, "attractor_escape": convergence_suppressed}
