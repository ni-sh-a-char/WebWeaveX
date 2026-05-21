from __future__ import annotations

import re
from typing import Any, Dict, List


def parse_rust_ast(source: str, path: str = "") -> Dict[str, Any]:
    nodes = [{"name": m.group(1), "kind": "fn"} for m in re.finditer(r"fn\s+(\w+)", source)]
    imports = [{"module": m.group(1), "kind": "use"} for m in re.finditer(r"use\s+([^;]+);", source)]
    return {
        "language": "rust",
        "path": path,
        "nodes": sorted(nodes, key=lambda item: item["name"])[:5000],
        "imports": sorted(imports, key=lambda item: item["module"])[:2000],
        "calls": [],
        "bounded": True,
    }
