from __future__ import annotations

def split_seeds(seeds: list, shards: int = 2):
    data=sorted(set(seeds or []))
    out=[[] for _ in range(max(1,shards))]
    for i,s in enumerate(data): out[i % len(out)].append(s)
    return out
