from __future__ import annotations

def build_lineage(paths: list):
    paths = sorted(set(paths or []))
    edges=[]
    for p in paths:
        parts=p.split('/')
        for i in range(1,len(parts)):
            edges.append({"from": '/'.join(parts[:i]), "to": '/'.join(parts[:i+1])})
    edges=sorted({(e['from'],e['to']) for e in edges})
    return {"nodes": sorted(set(paths + [x for e in edges for x in e])), "edges": [{"from":a,"to":b} for a,b in edges]}
