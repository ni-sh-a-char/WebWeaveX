from __future__ import annotations
from urllib.parse import urlparse, urlunparse

def canonicalize_sources(urls: list[str]):
    out = []
    for u in sorted(set(urls or [])):
        p = urlparse(u)
        norm = urlunparse((p.scheme.lower(), p.netloc.lower(), p.path or '/', '', '', ''))
        out.append(norm)
    return sorted(set(out))
