from __future__ import annotations
from urllib.parse import urlparse, urlunparse

def canonicalize_source_set(urls: list[str]):
    out = []
    for u in sorted(set(urls or [])):
        p = urlparse(u)
        out.append(urlunparse((p.scheme.lower(), p.netloc.lower(), p.path or '/', '', '', '')))
    return sorted(set(out))
