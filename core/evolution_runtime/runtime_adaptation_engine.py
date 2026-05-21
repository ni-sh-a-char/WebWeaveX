from __future__ import annotations

from typing import Any, Dict


def adapt_runtime_strategy(
    strategy: Dict[str, Any],
    optimization: Dict[str, Any],
) -> Dict[str, Any]:
    adapted = dict(strategy)
    if optimization.get("convergence_gain"):
        adapted["synchronization_path"] = "continuous"
    if optimization.get("runtime_pressure", 0) > 0:
        adapted["extraction_path"] = "repair_then_extract"
    adapted["adapted"] = True
    adapted["bounded"] = True
    return adapted
