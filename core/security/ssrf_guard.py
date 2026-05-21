from __future__ import annotations
from core.security.url_validator import is_safe_url
def safe_remote_url(url:str):
    return is_safe_url(url)
