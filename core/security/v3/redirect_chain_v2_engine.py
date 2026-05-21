from __future__ import annotations

from urllib.parse import urlparse


def validate_redirect_chain_v3(urls: list[str], max_hops: int = 10):
    chain = urls or []
    safe = True
    if len(chain) > max_hops:
        safe = False
    for u in chain:
        scheme = (urlparse(u).scheme or "").lower()
        if scheme in {"file", "ftp", "gopher", "smb"}:
            safe = False
            break
    return {"allowed": safe, "hops": len(chain), "max_hops": max_hops}
