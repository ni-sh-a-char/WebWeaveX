from __future__ import annotations

from typing import Any, Dict

MAX_SHEETS = 500
MAX_ROWS = 10000


def extract_spreadsheet_structure(
    workbook: Dict[str, Any],
) -> Dict[str, Any]:
    sheets = []

    for name, rows in list(
        workbook.items()
    )[:MAX_SHEETS]:
        sheets.append({
            "sheet": name,
            "rows": rows[:MAX_ROWS],
        })

    return {
        "worksheets": sheets,
        "bounded": True,
    }
