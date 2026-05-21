from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_NAV = 500


def build_navigation_semantics(
    html: str,
    route: str,
    route_history: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")
    menus: List[Dict[str, Any]] = []
    breadcrumbs: List[str] = []

    for nav in soup.find_all("nav")[:MAX_NAV]:
        for link in nav.find_all("a"):
            href = str(link.get("href", ""))[:500]
            if href:
                menus.append({
                    "href": href,
                    "text": link.get_text(strip=True)[:200],
                })

    for crumb in soup.find_all(class_=lambda value: value and "breadcrumb" in value)[:MAX_NAV]:
        breadcrumbs.append(crumb.get_text(strip=True)[:500])

    routes = [{"path": route, "order": 0}]
    if route_history:
        routes = list(route_history)[:MAX_NAV]

    tabs = []
    for tab in soup.find_all(attrs={"role": "tab"})[:MAX_NAV]:
        tabs.append({
            "label": tab.get_text(strip=True)[:200],
        })

    return {
        "menus": sorted(menus, key=lambda item: item.get("href", "")),
        "breadcrumbs": breadcrumbs,
        "routes": routes,
        "spa_transitions": len(routes) > 1,
        "tab_hierarchy": tabs,
        "bounded": True,
    }
