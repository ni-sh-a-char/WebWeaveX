from __future__ import annotations

from typing import Any, Dict


def compile_reconstruction_runtime_ir(
    reconstruction_payload: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "reconstruction_runtime",
        "reconstructed_runtimes": reconstruction_payload.get("runtime", {}),
        "replay_chains": reconstruction_payload.get("replay", {}).get("replay_chains", []),
        "topology": reconstruction_payload.get("topology", {}),
        "runtime_identities": reconstruction_payload.get("identity", {}),
        "fabricated_environments": reconstruction_payload.get("fabrication", {}),
        "execution_continuity": reconstruction_payload.get("state", {}),
        "validation": reconstruction_payload.get("validation", {}),
        "browser": reconstruction_payload.get("browser", {}),
        "application": reconstruction_payload.get("application", {}),
        "timeline": reconstruction_payload.get("timeline", {}),
        "clone": reconstruction_payload.get("clone", {}),
        "bounded": True,
    }


def reconstruction_runtime_ir_to_graph(
    reconstruction_ir: Dict[str, Any],
) -> Dict[str, Any]:
    nodes = [{"id": "reconstruction:root", "type": "reconstruction"}]
    edges = []

    runtime = reconstruction_ir.get("reconstructed_runtimes", {})
    runtime_id = str(runtime.get("runtime_id", ""))
    if runtime_id:
        nodes.append({"id": f"runtime:{runtime_id}", "type": "runtime"})
        edges.append({
            "from": "reconstruction:root",
            "to": f"runtime:{runtime_id}",
            "relation": "reconstructs",
        })

    for index, chain in enumerate(reconstruction_ir.get("replay_chains", [])[:10000]):
        step_id = str(chain.get("action_id", f"step:{index}"))
        node_id = f"replay:{step_id}"
        nodes.append({"id": node_id, "type": "replay"})
        edges.append({
            "from": node_id,
            "to": "reconstruction:root",
            "relation": "replays",
        })

    fabrication = reconstruction_ir.get("fabricated_environments", {})
    if fabrication.get("fabricated"):
        nodes.append({"id": "fabrication:reality", "type": "fabrication"})
        edges.append({
            "from": "fabrication:reality",
            "to": "reconstruction:root",
            "relation": "fabricates",
        })

    clone = reconstruction_ir.get("clone", {})
    if clone.get("cloned"):
        nodes.append({"id": "clone:environment", "type": "clone"})
        edges.append({
            "from": "clone:environment",
            "to": "reconstruction:root",
            "relation": "clones",
        })

    graph = reconstruction_ir.get("topology", {}).get("runtime_graph", {})
    for node in graph.get("nodes", [])[:5000]:
        node_id = str(node.get("id", ""))
        if node_id:
            nodes.append({"id": node_id, "type": str(node.get("type", "node"))})

    return {
        "ir": "reconstruction_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
