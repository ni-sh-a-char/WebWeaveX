from __future__ import annotations

from typing import Any, Dict


def suppress_worldview_convergence(convergence: bool, depth: int) -> Dict[str, Any]:
    return {"convergence": convergence and depth >= 2, "suppress": convergence, "lock_in_prevented": True}
