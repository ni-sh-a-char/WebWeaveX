from __future__ import annotations

def source_consensus(sources: list[dict]):
    votes = {}
    for s in sources or []:
        for k, v in sorted((s or {}).items()):
            votes.setdefault((k, str(v)), 0)
            votes[(k, str(v))] += 1
    consensus = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))
    return {"consensus": [{"field": k[0], "value": k[1], "votes": n} for k, n in consensus[:20]]}
