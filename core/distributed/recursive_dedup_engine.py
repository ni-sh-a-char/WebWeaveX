from __future__ import annotations


def recursive_dedup(urls: list[str]):
    return sorted(set(urls or []))
