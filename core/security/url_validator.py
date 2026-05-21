from __future__ import annotations

from urllib.parse import urlparse
import ipaddress

ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_SCHEMES = {"file", "smb", "ftp"}


def is_safe_url(url: str) -> bool:
    try:
        p = urlparse(url)
        if p.scheme in BLOCKED_SCHEMES:
            return False
        if p.scheme not in ALLOWED_SCHEMES or not p.hostname:
            return False
        host = p.hostname.lower()
        if host in {"localhost", "127.0.0.1"}:
            return False
        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return False
        except ValueError:
            pass
        return True
    except Exception:
        return False
