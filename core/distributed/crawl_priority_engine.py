from __future__ import annotations

from urllib.parse import urlparse


def prioritize_crawl_frontier(urls: list[str]):
    def score(u: str):
        p = urlparse(u)
        path_depth = len([x for x in p.path.split("/") if x])
        return (p.netloc, path_depth, p.path, u)

    return sorted(set(urls or []), key=score)
