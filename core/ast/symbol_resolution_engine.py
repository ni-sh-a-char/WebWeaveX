from __future__ import annotations

from typing import Any, Dict, List


def resolve_symbols(ast_ir: Dict[str, Any]) -> Dict[str, Any]:

    symbols: List[Dict[str, Any]] = []

    for fn in ast_ir.get("functions", []):
        symbols.append({
            "symbol": fn["name"],
            "kind": "function",
            "args": fn.get("args", []),
        })

    for cls in ast_ir.get("classes", []):
        symbols.append({
            "symbol": cls["name"],
            "kind": "class",
            "bases": cls.get("bases", []),
        })

    return {
        "symbols": sorted(symbols, key=lambda x: x["symbol"]),
        "symbol_count": len(symbols),
        "grounded": True,
    }
