from __future__ import annotations
import re

def build_concept_graph(text: str):
    concepts = sorted(set(re.findall(r'`([^`]+)`', text or '')))
    edges = [{"from": concepts[i], "to": concepts[i+1]} for i in range(max(0, len(concepts)-1))]
    return {"nodes": concepts, "edges": edges}
