from __future__ import annotations


def compute_freshness_v2(previous_content_hashes: dict, current_content_hashes: dict):
    prev = previous_content_hashes or {}
    curr = current_content_hashes or {}
    changed = sorted([u for u in sorted(curr) if prev.get(u) != curr.get(u)])
    unchanged = sorted([u for u in sorted(curr) if prev.get(u) == curr.get(u)])
    return {"changed": changed, "unchanged": unchanged}
