from __future__ import annotations

from typing import Any, Dict, List


def reconstruct_execution_flow(parsed: Dict[str, Any]) -> Dict[str, Any]:
    sym = (parsed or {}).get("symbols", {}) or {}
    funcs = sym.get("functions", []) if isinstance(sym, dict) else []
    calls = ((parsed or {}).get("calls", {}) or {}).get("calls", []) or []
    entrypoints = [f for f in funcs if str(f).startswith(("main", "run_", "handle_"))]
    flow = [{"step": i, "call": c} for i, c in enumerate(calls[:50]) if isinstance(c, dict)]
    return {
        "entrypoints": entrypoints[:20],
        "flow": flow,
        "evidence": ["parser:functions", "parser:call_graph"] if funcs else [],
    }
