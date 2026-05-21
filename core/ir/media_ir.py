from __future__ import annotations

from typing import Any, Dict


def compile_media_ir(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ir": "media",
        "content": payload,
        "bounded": True,
    }
