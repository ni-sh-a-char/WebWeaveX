from __future__ import annotations

from typing import Any, Dict


def diffuse_recursive_authority(interpretation_count: int) -> Dict[str, Any]:
    return {"diffused": interpretation_count > 1, "concentration_blocked": interpretation_count <= 1}
