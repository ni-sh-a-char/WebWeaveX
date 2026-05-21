from __future__ import annotations


def build_distributed_frontier_v2(urls: list[str]):
    return sorted(set(urls or []))
