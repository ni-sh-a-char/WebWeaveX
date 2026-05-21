from __future__ import annotations

from typing import Any, Dict

from core.runtime_language.wwx_compiler import compile_wwx
from core.runtime_language.wwx_parser import parse_wwx


def interpret_wwx(source: str, tick: int = 0) -> Dict[str, Any]:
    parsed = parse_wwx(source)
    compiled = compile_wwx(parsed)
    results = []
    for step in compiled.get("plan", {}).get("steps", []):
        results.append({
            "action": step["action"],
            "target": step["target"],
            "simulated": step["action"] in ("extract", "sync", "replay"),
            "tick": tick,
            "executed": step["action"] == "execute",
        })
    return {
        "parsed": parsed,
        "compiled": compiled,
        "results": results,
        "deterministic": True,
        "bounded": True,
    }
