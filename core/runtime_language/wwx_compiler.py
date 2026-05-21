from __future__ import annotations

from typing import Any, Dict

from core.runtime_language.wwx_validator import validate_wwx


def compile_wwx(parsed: Dict[str, Any]) -> Dict[str, Any]:
    validation = validate_wwx(parsed)
    plan = {
        "steps": [
            {
                "action": stmt["verb"].lower(),
                "target": stmt["target"],
                "args": stmt.get("args", []),
            }
            for stmt in parsed.get("statements", [])
        ],
        "deterministic": True,
    }
    return {
        "plan": plan,
        "validation": validation,
        "compiled": validation["valid"],
        "bounded": True,
    }
