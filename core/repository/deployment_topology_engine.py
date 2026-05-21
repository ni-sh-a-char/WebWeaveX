from __future__ import annotations

import re
from typing import Dict, List

from core.repository.topology_cognition_engine import build_topology_cognition


def infer_deployment_topology(text: str) -> Dict[str, object]:
    src = text or ""
    targets: List[str] = []
    for pat in (
        r"image:\s*([^\s]+)",
        r"container_name:\s*([^\s]+)",
        r"deployment\.kubernetes\.io/([^\s]+)",
        r"helm\s+install\s+([^\s]+)",
    ):
        targets.extend(re.findall(pat, src, flags=re.IGNORECASE))
    observed_nodes = sorted(set(targets))
    cognition = build_topology_cognition(text, path="deploy.yaml", observed_nodes=observed_nodes, inferred_nodes=observed_nodes)
    cognition["deployments"] = observed_nodes
    cognition["evidence"] = sorted(set((cognition.get("evidence") or []) + ["manifest_patterns"]))
    return cognition
