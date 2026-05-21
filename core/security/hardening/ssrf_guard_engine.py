from __future__ import annotations
from urllib.parse import urlparse
import ipaddress

def ssrf_guard(url: str):
    p=urlparse(url or '')
    if p.scheme.lower() not in {'http','https'}:
        return {"ok": False}
    host=(p.hostname or '').lower()
    if host in {'localhost','127.0.0.1','::1'}:
        return {"ok": False}
    try:
        ip=ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback:
            return {"ok": False}
    except ValueError:
        pass
    return {"ok": True}
