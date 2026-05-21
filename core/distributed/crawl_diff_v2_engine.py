from __future__ import annotations


def compute_crawl_diff_v2(previous: list[str], current: list[str]):
    p = set(previous or [])
    c = set(current or [])
    return {"added": sorted(c - p), "removed": sorted(p - c), "unchanged": sorted(c & p)}
