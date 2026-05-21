from __future__ import annotations

from typing import Any, Dict


def create_session() -> Dict[str, Any]:
    return {
        "cookies": [],
        "headers": {},
        "authenticated": False,
        "bounded": True,
    }
