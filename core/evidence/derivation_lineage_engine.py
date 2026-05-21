from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.lineage_engine import build_lineage


def track_derivation(steps: List[str], inputs: List[str], outputs: List[str]) -> Dict[str, Any]:
    stages = [
        {"stage": step, "inputs": sorted(inputs), "outputs": sorted(outputs)}
        for step in sorted(set(steps or []))
    ]
    return build_lineage(stages)
