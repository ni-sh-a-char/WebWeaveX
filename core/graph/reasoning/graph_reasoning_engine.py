from __future__ import annotations

def graph_reason(graph: dict):
    deg={}
    for e in (graph or {}).get('edges',[]):
        if not isinstance(e,dict): continue
        deg[e.get('from')]=deg.get(e.get('from'),0)+1
        deg[e.get('to')]=deg.get(e.get('to'),0)+1
    hubs=sorted([k for k in deg if k], key=lambda n:(-deg[n],n))[:20]
    return {"connected": len((graph or {}).get('edges',[]))>0, "hubs":[{"node":h,"degree":deg[h]} for h in hubs]}
