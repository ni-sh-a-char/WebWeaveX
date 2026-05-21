from __future__ import annotations

from typing import Any, Dict, List


MAX_SHARDS = 64


def reconstruct_distributed_execution(
    shards: List[Dict[str, Any]],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    ordered = sorted(shards, key=lambda s: str(s.get("id", "")))[:MAX_SHARDS]
    return {
        "shards": ordered,
        "shard_count": len(ordered),
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
        "bounded": len(ordered) <= MAX_SHARDS,
    }
