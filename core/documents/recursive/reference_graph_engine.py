from __future__ import annotations

from core.documents.reference_engine import extract_references


def build_reference_graph(text: str):
    refs = extract_references(text)
    nodes = sorted(set(["document"] + refs.get("external_links", []) + refs.get("internal_links", [])))
    edges = [{"from": "document", "to": n} for n in nodes if n != "document"]
    edges = sorted(edges, key=lambda x: (x["from"], x["to"]))
    return {"nodes": nodes, "edges": edges}

