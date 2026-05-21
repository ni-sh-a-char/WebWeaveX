from __future__ import annotations

def reconstruct_domain_model(modules: list[str]):
    domains = {}
    for m in sorted(set(modules or [])):
        key = m.split('/')[0] if '/' in m else m
        domains.setdefault(key, []).append(m)
    return {"domains": [{"name": k, "modules": sorted(v)} for k, v in sorted(domains.items())]}
