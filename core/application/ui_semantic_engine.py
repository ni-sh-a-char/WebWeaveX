from __future__ import annotations

import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_ITEMS = 1000


def extract_ui_semantics(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")
    semantics: Dict[str, List[Dict[str, Any]]] = {
        "dashboards": [],
        "forms": [],
        "navigation_menus": [],
        "tables": [],
        "charts": [],
        "filters": [],
        "search_bars": [],
        "sidebars": [],
        "tabs": [],
    }

    for form in soup.find_all("form")[:MAX_ITEMS]:
        semantics["forms"].append({
            "action": str(form.get("action", ""))[:500],
            "id": str(form.get("id", ""))[:200],
        })

    for nav in soup.find_all(["nav", "header"])[:MAX_ITEMS]:
        semantics["navigation_menus"].append({
            "tag": nav.name,
            "links": len(nav.find_all("a")),
        })

    for table in soup.find_all("table")[:MAX_ITEMS]:
        semantics["tables"].append({
            "rows": len(table.find_all("tr")),
        })

    if re.search(r"dashboard|metrics|kpi", html, re.IGNORECASE):
        semantics["dashboards"].append({"detected": True})

    for canvas in soup.find_all("canvas")[:MAX_ITEMS]:
        semantics["charts"].append({"type": "canvas"})

    for node in soup.find_all(["input", "select"])[:MAX_ITEMS]:
        node_type = str(node.get("type", "")).lower()
        if node_type in {"search", "text"} and "search" in str(node.get("name", "")).lower():
            semantics["search_bars"].append({
                "name": str(node.get("name", ""))[:200],
            })
        elif node_type in {"select", "checkbox", "radio"}:
            semantics["filters"].append({
                "type": node_type,
                "name": str(node.get("name", ""))[:200],
            })

    for aside in soup.find_all("aside")[:MAX_ITEMS]:
        semantics["sidebars"].append({"tag": "aside"})

    for tab in soup.find_all(attrs={"role": "tab"})[:MAX_ITEMS]:
        semantics["tabs"].append({
            "label": tab.get_text(strip=True)[:200],
        })

    return {
        "semantics": semantics,
        "bounded": True,
    }
