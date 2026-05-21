from __future__ import annotations

def infer_ownership_domains(paths: list[str]):
    domains = {}
    for p in sorted(set(paths or [])):
        key = p.split('/')[0] if '/' in p else 'root'
        domains.setdefault(key, []).append(p)
    return {"domains": [{"name": k, "paths": sorted(v)} for k, v in sorted(domains.items())]}
