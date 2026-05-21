from __future__ import annotations

from typing import Dict, List
from urllib.parse import urlparse


def cluster_sources(urls: List[str]) -> Dict[str, object]:
    clusters: Dict[str, List[str]] = {}
    for url in sorted(set(urls or [])):
        host = urlparse(url).netloc.lower() or "unknown"
        clusters.setdefault(host, []).append(url)
    return {
        "clusters": [{"host": h, "urls": sorted(u)} for h, u in sorted(clusters.items())],
        "cluster_count": len(clusters),
    }
