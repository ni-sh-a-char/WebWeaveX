from __future__ import annotations

def _adj(graph: dict):
    a = {}
    for e in (graph or {}).get('edges', []):
        if not isinstance(e, dict):
            continue
        f, t = e.get('from',''), e.get('to','')
        if f and t:
            a.setdefault(f, []).append(t)
    for k in a:
        a[k] = sorted(set(a[k]))
    return a


def semantic_paths(graph: dict, start: str, depth: int = 3):
    adj = _adj(graph)
    paths = []
    q = [(start, [start], 0)]
    while q:
        cur, path, d = q.pop(0)
        if d >= depth:
            paths.append(path)
            continue
        nxts = adj.get(cur, [])
        if not nxts:
            paths.append(path)
        for n in nxts:
            if n in path:
                continue
            q.append((n, path + [n], d + 1))
    return {"paths": sorted(paths)}
