from __future__ import annotations

def graph_diff(a: dict, b: dict):
    ae=set((e.get('from'),e.get('to')) for e in (a or {}).get('edges',[]) if isinstance(e,dict))
    be=set((e.get('from'),e.get('to')) for e in (b or {}).get('edges',[]) if isinstance(e,dict))
    return {"added_edges":[{"from":f,"to":t} for f,t in sorted(be-ae)],"removed_edges":[{"from":f,"to":t} for f,t in sorted(ae-be)]}
