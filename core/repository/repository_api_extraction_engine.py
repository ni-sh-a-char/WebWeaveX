from __future__ import annotations

import re
from typing import Any, Dict, List

ROUTE_PATTERNS = [
    re.compile(r'@app\.route\(["\']([^"\']+)'),
    re.compile(
        r'router\.(get|post|put|delete|patch)\(["\']([^"\']+)'
    ),
    re.compile(r'@(?:get|post|put|delete|patch)\(["\']([^"\']+)'),
]

MAX_ROUTES = 10000
MAX_SOURCE_BYTES = 500_000


def extract_repository_apis(
    source: str,
) -> Dict[str, Any]:
    routes: List[str] = []

    for pattern in ROUTE_PATTERNS:
        for match in pattern.findall(source):
            if isinstance(match, tuple):
                route = match[-1]
            else:
                route = match

            routes.append(str(route))

            if len(routes) >= MAX_ROUTES:
                break

    return {
        "routes": sorted(set(routes)),
        "bounded": True,
    }


def extract_repository_api_index(
    files: List[Dict[str, Any]],
) -> Dict[str, Any]:
    routes: List[str] = []
    per_file: List[Dict[str, Any]] = []

    for file in files:
        if file.get("extension") != ".py":
            continue

        try:
            with open(
                file["path"],
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as handle:
                source = handle.read(MAX_SOURCE_BYTES)
        except OSError:
            continue

        found = extract_repository_apis(source)
        file_routes = found.get("routes", [])
        if file_routes:
            per_file.append({
                "path": file["path"],
                "routes": file_routes,
            })
            routes.extend(file_routes)

    return {
        "routes": sorted(set(routes))[:MAX_ROUTES],
        "per_file": sorted(per_file, key=lambda x: x["path"]),
        "bounded": True,
    }
