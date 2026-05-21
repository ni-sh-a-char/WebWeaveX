from __future__ import annotations

import hashlib


def balance_shards_deterministically(urls: list[str], shard_count: int = 4):
    shard_count = max(1, int(shard_count))
    shards = {str(i): [] for i in range(shard_count)}
    for u in sorted(set(urls or [])):
        h = int(hashlib.sha256(u.encode("utf-8")).hexdigest(), 16)
        idx = str(h % shard_count)
        shards[idx].append(u)
    return {k: sorted(v) for k, v in sorted(shards.items())}
