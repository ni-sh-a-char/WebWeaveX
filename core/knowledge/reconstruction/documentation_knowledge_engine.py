from __future__ import annotations


def build_documentation_knowledge(docs: dict):
    sections = [str(s) for s in docs.get("sections", [])]
    refs_raw = docs.get("references", [])
    refs = []
    for r in refs_raw:
        if isinstance(r, dict):
            refs.append(f"{r.get('method','')} {r.get('path','')}".strip())
        else:
            refs.append(str(r))
    nodes = sorted(set([x for x in sections + refs if x]))
    edges = [{"from": "doc", "to": n} for n in nodes]
    return {"nodes": nodes, "edges": edges}
