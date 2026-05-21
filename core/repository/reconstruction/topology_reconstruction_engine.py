from __future__ import annotations

def reconstruct_topology(paths: list[str]):
    modules = sorted(set(paths or []))
    services = sorted(set([p.split('/')[0] for p in modules if '/' in p]))
    layers = sorted(set([p.split('/')[1] for p in modules if p.count('/') >= 2]))
    boundaries = sorted(set([p.rsplit('/', 1)[0] for p in modules if '/' in p]))
    return {"modules": modules, "services": services, "layers": layers, "boundaries": boundaries}
