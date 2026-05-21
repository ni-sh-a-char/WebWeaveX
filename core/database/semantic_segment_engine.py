from __future__ import annotations

import json
from pathlib import Path

from typing import Any, Dict, List


MAX_SEGMENT_SIZE = 10000


def write_semantic_segment(
    path: str,
    records: List[Dict[str, Any]],
) -> Dict[str, Any]:

    bounded = records[:MAX_SEGMENT_SIZE]

    target = Path(path)

    target.write_text(
        json.dumps(
            bounded,
            sort_keys=True,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    return {
        "records": len(bounded),
        "path": str(target),
    }
