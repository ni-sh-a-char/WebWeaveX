from __future__ import annotations

from typing import Any, Dict


def run_identity_phase(identity: Dict[str, Any]) -> Dict[str, Any]:
    from core.identity.browser_identity_engine import build_browser_identity

    built = build_browser_identity(str(identity.get("profile", "default")))
    return {"identity": {**built, **identity}, "bounded": True}
