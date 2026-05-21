from __future__ import annotations

from typing import Any, Dict

from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload


def build_canvas_runtime(profile_id: str = "default") -> Dict[str, Any]:
    payload = {
        "profile_id": profile_id,
        "canvas_seed": f"webweavex-canvas:{profile_id}",
    }
    fingerprint = compute_kaalka_hash_payload(payload)

    return {
        "canvas_fingerprint": fingerprint,
        "canvas_seed": payload["canvas_seed"],
        "bounded": True,
    }
