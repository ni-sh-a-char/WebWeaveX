from __future__ import annotations

from ._helpers import node_ids


def graph_similarity(a: dict, b: dict):
    an = set(node_ids(a))
    bn = set(node_ids(b))
    ae = set(
        (e.get("from"), e.get("to"))
        for e in (a or {}).get("edges", [])
        if isinstance(e, dict)
    )
    be = set(
        (e.get("from"), e.get("to"))
        for e in (b or {}).get("edges", [])
        if isinstance(e, dict)
    )
    ns = 1.0 if not (an | bn) else len(an & bn) / len(an | bn)
    es = 1.0 if not (ae | be) else len(ae & be) / len(ae | be)
    return {"node": ns, "edge": es, "score": round((ns + es) / 2, 6)}
