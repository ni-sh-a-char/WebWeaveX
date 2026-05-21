from __future__ import annotations

import re
from typing import Any, Dict, List


def parse_java_ast(source: str, path: str = "") -> Dict[str, Any]:
    imports = [{"module": m.group(1), "kind": "java_import"} for m in re.finditer(r"import\s+([\w.]+);", source)]
    nodes = [{"name": m.group(1), "kind": "class"} for m in re.finditer(r"class\s+(\w+)", source)]
    calls = [{"target": m.group(1), "kind": "call"} for m in re.finditer(r"(\w+)\s*\(", source)]
    return {
        "language": "java",
        "path": path,
        "nodes": sorted(nodes, key=lambda item: item["name"])[:5000],
        "imports": sorted(imports, key=lambda item: item["module"])[:2000],
        "calls": sorted(calls, key=lambda item: item["target"])[:5000],
        "bounded": True,
    }
