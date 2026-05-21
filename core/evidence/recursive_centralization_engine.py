from __future__ import annotations

from typing import Any, Dict


def detect_recursive_centralization(decentralized: bool, depth: int) -> Dict[str, Any]:
    centralized = not decentralized and depth >= 2
    return {"centralized": centralized, "suppress": centralized}
