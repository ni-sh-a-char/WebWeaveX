from __future__ import annotations

def build_concept_graph(concepts: list[str]):
    c=sorted(set(concepts or []))
    return {"nodes": c, "edges":[{"from":c[i],"to":c[i+1]} for i in range(max(0,len(c)-1))]}
