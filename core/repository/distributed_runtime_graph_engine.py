from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.repository.semantic_runtime_graph_engine import build_semantic_runtime_graph


def build_distributed_runtime_graph(source: str, path: str = "", files: Optional[List[str]] = None) -> Dict[str, Any]:
    g = build_semantic_runtime_graph(source, path, files)
    shards = {}
    for i, node in enumerate(g.get("nodes", [])[:20]):
        shards[f"shard_{i % 4}"] = shards.get(f"shard_{i % 4}", []) + [node]
    return {**g, "shards": shards, "distributed": True, "evidence": g.get("evidence", [])}
