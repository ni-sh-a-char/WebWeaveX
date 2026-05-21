from __future__ import annotations

from typing import Dict, Any


def infer_architecture(topology: Dict[str, Any], import_graph: Dict[str, Any]) -> Dict[str, Any]:
    modules = topology.get("modules", [])
    layers = sorted(set([m.split('/')[0] for m in modules if '/' in m]))
    components = sorted(set([m.rsplit('/', 1)[-1] for m in modules]))
    relationships = sorted(import_graph.get("edges", []), key=lambda x: (x.get("from", ""), x.get("to", "")))
    return {"layers": layers, "components": components, "relationships": relationships}
