from __future__ import annotations

import json

from pathlib import Path

from typing import Any, Dict


def write_semantic_storage(
    path: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:

    p = Path(path)

    encoded = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        default=str,
    )

    p.write_text(
        encoded,
        encoding="utf-8",
    )

    return {
        "path": str(p),
        "written": True,
        "bytes": len(encoded),
    }
