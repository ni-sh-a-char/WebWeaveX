from __future__ import annotations
def shard_urls(urls:list, shards:int=2):
    data=sorted(set(urls or [])); out=[[] for _ in range(max(1,shards))]
    for i,u in enumerate(data): out[i%len(out)].append(u)
    return out
