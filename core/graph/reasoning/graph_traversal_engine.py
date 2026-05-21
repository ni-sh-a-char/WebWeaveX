from __future__ import annotations

def graph_traverse(graph: dict, start: str, max_steps: int = 1000):
    adj={}
    for e in (graph or {}).get('edges',[]):
        if not isinstance(e,dict): continue
        f,t=e.get('from',''),e.get('to','')
        if f and t: adj.setdefault(f,[]).append(t)
    for k in adj: adj[k]=sorted(set(adj[k]))
    order=[]; q=[start]; seen=set([start])
    while q and len(order)<max_steps:
        cur=q.pop(0); order.append(cur)
        for nxt in adj.get(cur,[]):
            if nxt in seen: continue
            seen.add(nxt); q.append(nxt)
    return {"order": order}
