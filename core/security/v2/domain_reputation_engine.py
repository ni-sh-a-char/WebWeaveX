from __future__ import annotations
def domain_allowed(domain:str, blocklist=None):
    b=set(blocklist or []); return (domain or "") not in b
