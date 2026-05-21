from __future__ import annotations

from typing import Any, Dict


def build_query_ast(parsed: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "semantic_query",
        "select": parsed.get("select", []),
        "where": parsed.get("where", {}),
        "limit": parsed.get("limit", 100),
    }
