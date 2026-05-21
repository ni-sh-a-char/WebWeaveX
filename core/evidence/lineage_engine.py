from __future__ import annotations

from typing import Any, Dict, List


def build_lineage(stages: List[Dict[str, Any]]) -> Dict[str, Any]:
    chain = []
    for idx, stage in enumerate(stages or []):
        if not isinstance(stage, dict):
            continue
        chain.append(
            {
                "step": idx,
                "stage": stage.get("stage", f"step_{idx}"),
                "inputs": sorted(stage.get("inputs", [])) if isinstance(stage.get("inputs"), list) else [],
                "outputs": sorted(stage.get("outputs", [])) if isinstance(stage.get("outputs"), list) else [],
            }
        )
    return {"stages": chain, "depth": len(chain)}
