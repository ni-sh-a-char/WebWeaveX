from __future__ import annotations

from typing import Any, Dict


def plan_semantic_query(ast: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "steps": [
            {
                "operation": "scan",
                "filters": ast.get("where", {}),
            },
            {
                "operation": "project",
                "fields": ast.get("select", []),
            },
        ],
        "limit": ast.get("limit", 100),
    }
