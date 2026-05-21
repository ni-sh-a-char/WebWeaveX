from __future__ import annotations

from typing import Any, Dict, List

MAX_TABLES = 1000
MAX_ROWS = 10000


def extract_document_tables(
    text: str,
) -> Dict[str, Any]:
    tables = []

    rows = []

    for line in text.splitlines():
        if "|" in line:
            rows.append([
                x.strip()
                for x in line.split("|")
            ])

    if rows:
        tables.append({
            "rows": rows[:MAX_ROWS],
        })

    return {
        "tables": tables[:MAX_TABLES],
        "bounded": True,
    }
