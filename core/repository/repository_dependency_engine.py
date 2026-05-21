from __future__ import annotations

import re
from typing import Any, Dict, List

IMPORT_RE = re.compile(
    r"^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)",
    re.MULTILINE,
)

MAX_IMPORTS = 10000
MAX_SOURCE_BYTES = 500_000


def extract_dependencies(
    source: str,
) -> Dict[str, Any]:
    imports: List[str] = []

    for match in IMPORT_RE.findall(source):
        imports.append(match)

        if len(imports) >= MAX_IMPORTS:
            break

    return {
        "imports": sorted(set(imports)),
        "bounded": True,
    }


def extract_repository_dependencies(
    files: List[Dict[str, Any]],
) -> Dict[str, Any]:
    all_imports: List[str] = []
    per_file: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for file in files:
        if not file.get("supported_code"):
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

        deps = extract_dependencies(source)
        imports = deps.get("imports", [])
        per_file.append({
            "path": file["path"],
            "imports": imports,
        })
        all_imports.extend(imports)

        for imp in imports:
            edges.append({
                "from": file["path"],
                "to": imp,
                "relation": "imports",
            })

    return {
        "imports": sorted(set(all_imports))[:MAX_IMPORTS],
        "per_file": sorted(per_file, key=lambda x: x["path"]),
        "edges": sorted(
            edges[:MAX_IMPORTS],
            key=lambda x: (
                str(x.get("from")),
                str(x.get("to")),
            ),
        ),
        "bounded": True,
    }
