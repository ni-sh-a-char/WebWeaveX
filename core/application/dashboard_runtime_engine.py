from __future__ import annotations

import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_WIDGETS = 1000


def build_dashboard_runtime(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")
    widgets: List[Dict[str, Any]] = []
    tables: List[Dict[str, Any]] = []
    filters: List[Dict[str, Any]] = []
    charts: List[Dict[str, Any]] = []

    for node in soup.find_all(class_=re.compile(r"widget|card|metric|kpi", re.I))[:MAX_WIDGETS]:
        widgets.append({
            "text": node.get_text(strip=True)[:500],
            "tag": node.name,
        })

    for table in soup.find_all("table")[:MAX_WIDGETS]:
        tables.append({
            "rows": len(table.find_all("tr")),
            "columns": len(table.find_all("th")),
        })

    for select in soup.find_all("select")[:MAX_WIDGETS]:
        filters.append({
            "name": str(select.get("name", ""))[:200],
        })

    for canvas in soup.find_all("canvas")[:MAX_WIDGETS]:
        charts.append({
            "type": "canvas",
            "live": canvas.has_attr("data-live"),
        })

    return {
        "widgets": widgets,
        "metrics": [w for w in widgets if w.get("text")],
        "tables": tables,
        "filters": filters,
        "charts": charts,
        "update_interval": 30,
        "bounded": True,
    }
