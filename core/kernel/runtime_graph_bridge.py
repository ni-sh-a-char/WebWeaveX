from __future__ import annotations

from typing import Any, Dict, List


def merge_runtime_graph(irs: List[Dict[str, Any]]) -> Dict[str, Any]:
    from core.runtime_graph.runtime_graph_engine import build_runtime_graph

    return build_runtime_graph(irs)
