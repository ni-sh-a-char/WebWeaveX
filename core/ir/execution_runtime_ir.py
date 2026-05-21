from __future__ import annotations

from typing import Any, Dict


def compile_execution_runtime_ir(
    execution_payload: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "execution_runtime",
        "actions": execution_payload.get("actions", []),
        "queues": execution_payload.get("queue", {}),
        "transactions": execution_payload.get("transactions", []),
        "mutations": execution_payload.get("mutations", {}),
        "checkpoints": execution_payload.get("checkpoints", []),
        "federation": execution_payload.get("federation", {}),
        "synchronization": execution_payload.get("synchronization", {}),
        "execution_state": execution_payload.get("state", {}),
        "coordination": execution_payload.get("coordination", {}),
        "simulation": execution_payload.get("simulation", {}),
        "bounded": True,
    }


def execution_runtime_ir_to_graph(
    execution_ir: Dict[str, Any],
) -> Dict[str, Any]:
    nodes = [
        {"id": "execution:root", "type": "execution", "runtime": "operational"},
    ]
    edges = []

    for action in execution_ir.get("actions", [])[:10000]:
        action_id = str(action.get("id", action.get("action_id", "")))
        if not action_id:
            continue
        nodes.append({"id": f"action:{action_id}", "type": "action"})
        edges.append({
            "from": "execution:root",
            "to": f"action:{action_id}",
            "relation": "executes",
        })

    for route in execution_ir.get("federation", {}).get("execution_routes", [])[:10000]:
        worker_id = str(route.get("worker_id", ""))
        if worker_id:
            nodes.append({"id": f"worker:{worker_id}", "type": "worker"})
            edges.append({
                "from": f"worker:{worker_id}",
                "to": "execution:root",
                "relation": "coordinates",
            })

    for mutation in execution_ir.get("mutations", {}).get("mutations", [])[:10000]:
        target = str(mutation.get("target", mutation.get("kind", "mutation")))
        node_id = f"mutation:{target}"
        nodes.append({"id": node_id, "type": "mutation"})
        edges.append({
            "from": node_id,
            "to": "execution:root",
            "relation": "mutates",
        })

    return {
        "ir": "execution_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
