from __future__ import annotations


def build_semantic_relationships(sections: list, references: list):
    sec = sorted(set(sections or []))
    ref = sorted(set(references or []))
    edges = [{"from": s, "to": r} for s in sec for r in ref[:5]]
    return {"nodes": sorted(set(sec + ref)), "edges": sorted(edges, key=lambda x: (x["from"], x["to"]))}
