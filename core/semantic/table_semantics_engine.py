from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup


TABLE_KIND_RULES = [
    ("invoice", re.compile(r"invoice|amount due|billing", re.I)),
    ("ledger", re.compile(r"ledger|debit|credit|balance", re.I)),
    ("analytics", re.compile(r"metric|kpi|conversion|funnel", re.I)),
    ("transaction_log", re.compile(r"transaction|payment id|order id", re.I)),
    ("audit_trail", re.compile(r"audit|actor|timestamp|change", re.I)),
    ("monitoring_metrics", re.compile(r"cpu|memory|latency|uptime", re.I)),
    ("user_list", re.compile(r"user|email|role|status", re.I)),
    ("infrastructure_status", re.compile(r"host|node|cluster|health", re.I)),
]


def extract_table_semantics(
    html: str = "",
    headers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")
    headers = headers or []
    tables: List[Dict[str, Any]] = []

    for index, table in enumerate(soup.find_all("table")[:1000]):
        header_cells = [
            cell.get_text(strip=True)
            for cell in table.find_all("th")[:50]
        ]
        context = " ".join(header_cells + headers)[:2000]
        kinds = [
            kind for kind, pattern in TABLE_KIND_RULES if pattern.search(context)
        ]
        if not kinds:
            kinds = ["generic_table"]

        tables.append({
            "id": f"table:{index}",
            "kinds": sorted(kinds),
            "rows": len(table.find_all("tr")),
            "columns": len(header_cells),
        })

    return {
        "tables": tables,
        "primary_kind": tables[0]["kinds"][0] if tables else "none",
        "bounded": True,
    }
