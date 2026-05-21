from __future__ import annotations

from urllib.parse import urlparse

from core.security.url_validator import is_safe_url


def same_domain(seed: str, target: str) -> bool:
    try:
        return urlparse(seed).hostname == urlparse(target).hostname
    except Exception:
        return False


def allow_url(seed: str, url: str, same_domain_only: bool = False) -> bool:
    if not is_safe_url(url):
        return False
    if same_domain_only and not same_domain(seed, url):
        return False
    return True

