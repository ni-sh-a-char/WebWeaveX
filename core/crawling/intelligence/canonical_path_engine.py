from __future__ import annotations
from urllib.parse import urlparse, urlunparse

def canonical_paths(urls: list[str]):
    out=[]
    for u in sorted(set(urls or [])):
        p=urlparse(u)
        out.append(urlunparse((p.scheme.lower(), p.netloc.lower(), p.path or '/', '', '', '')))
    return sorted(set(out))
