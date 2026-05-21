from __future__ import annotations

import ipaddress
from urllib.parse import urlparse


def is_safe_remote_target(url: str) -> bool:
    parsed = urlparse(url or "")
    if parsed.scheme.lower() not in {"http", "https"}:
        return False
    host = (parsed.hostname or "").lower()
    if host in {"localhost", "127.0.0.1", "::1"}:
        return False
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        pass
    return True
