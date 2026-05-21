from __future__ import annotations

from typing import Any, Dict

from core.identity.browser_identity_orchestrator import build_browser_identity
from core.identity.browser_profile_engine import PROFILE_IDS


def rotate_browser_identity(
    identity: Dict[str, Any],
) -> Dict[str, Any]:
    current_index = int(identity.get("rotation_index", 0))
    next_index = (current_index + 1) % len(PROFILE_IDS)
    next_profile = PROFILE_IDS[next_index]

    rotated = build_browser_identity(next_profile)
    rotated["rotation_index"] = next_index
    rotated["previous_profile_id"] = identity.get("profile_id", "default")

    return rotated
