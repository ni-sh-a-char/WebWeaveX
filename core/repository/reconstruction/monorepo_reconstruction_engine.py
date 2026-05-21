from __future__ import annotations

def reconstruct_monorepo(paths: list[str]):
    p = sorted(set(paths or []))
    workspaces = [x for x in p if '/packages/' in x or x.startswith('packages/') or '/apps/' in x]
    groups = sorted(set([w.split('/')[0] for w in workspaces if '/' in w]))
    return {"workspaces": workspaces, "groups": groups}
