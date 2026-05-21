from __future__ import annotations

from typing import Any, Dict, List

MAX_ROWS = 1000


def extract_tables(
    layout_blocks: Dict[str, Any],
) -> Dict[str, Any]:
    tables = []

    current_rows = []

    for block in layout_blocks.get("blocks", []):
        text = block.get("text", "")

        if "|" in text:
            current_rows.append(
                [x.strip() for x in text.split("|")]
            )

    if current_rows:
        tables.append({
            "rows": current_rows[:MAX_ROWS],
        })

    return {
        "tables": tables,
        "bounded": True,
    }
