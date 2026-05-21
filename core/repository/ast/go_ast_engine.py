from __future__ import annotations

import re
from typing import Any, Dict, List


def parse_go_ast(source: str, path: str = "") -> Dict[str, Any]:
    imports = [{"module": m.group(1), "kind": "go_import"} for m in re.finditer(r'import\s+"([^"]+)"', source)]
    nodes = [{"name": m.group(1), "kind": "func"} for m in re.finditer(r"func\s+(\w+)", source)]
    return {
        "language": "go",
        "path": path,
        "nodes": sorted(nodes, key=lambda item: item["name"])[:5000],
        "imports": sorted(imports, key=lambda item: item["module"])[:2000],
        "calls": [],
        "bounded": True,
    }
