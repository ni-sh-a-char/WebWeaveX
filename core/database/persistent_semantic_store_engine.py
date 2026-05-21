from __future__ import annotations

import json
from pathlib import Path

from typing import Any, Dict


def persist_semantic_state(
    path: str,
    state: Dict[str, Any],
) -> Dict[str, Any]:

    target = Path(path)

    target.write_text(
        json.dumps(
            state,
            indent=2,
            sort_keys=True,
            default=str,
        ),
        encoding="utf-8",
    )

    return {
        "persisted": True,
        "path": str(target),
    }
