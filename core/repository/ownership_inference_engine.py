from __future__ import annotations

def infer_ownership(paths: list[str]):
    owners = {}
    for p in sorted(set(paths or [])):
        key = p.split('/')[0] if '/' in p else "root"
        owners.setdefault(key, []).append(p)
    return {"ownership": [{"team": k, "paths": sorted(v)} for k, v in sorted(owners.items())]}
