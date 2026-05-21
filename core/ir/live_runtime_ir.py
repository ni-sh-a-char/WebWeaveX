from __future__ import annotations

from typing import Any, Dict, List


def compile_live_runtime_ir(
    live: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "live_runtime",
        "database_topology": live.get("database", {}),
        "api_topology": live.get("api", {}),
        "stream_lineage": live.get("streams", {}),
        "filesystem": live.get("filesystem", {}),
        "containers": live.get("containers", {}),
        "kubernetes": live.get("kubernetes", {}),
        "cicd": live.get("cicd", {}),
        "telemetry": live.get("telemetry", {}),
        "ide": live.get("ide", {}),
        "graph": live.get("graph", {}),
        "synchronization": live.get("sync_state", {}),
        "bounded": True,
    }


def live_runtime_ir_to_graph(
    live_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = live_ir.get("graph", {})
    nodes = list(graph.get("nodes", []))
    edges = list(graph.get("edges", []))

    if not nodes:
        nodes = [{"id": "live:root", "type": "live_runtime"}]

    k8s = live_ir.get("kubernetes", {})
    for deploy in k8s.get("deployments", [])[:1000]:
        name = str(deploy.get("name", deploy) if isinstance(deploy, dict) else deploy)
        nodes.append({"id": f"k8s:deploy:{name}", "type": "deployment"})

    for stream in live_ir.get("stream_lineage", {}).get("streams", [])[:1000]:
        topics = stream.get("topics", [])
        if topics:
            nodes.append({
                "id": f"stream:{stream.get('stream_type', 'unknown')}:{topics[0]}",
                "type": "stream",
            })

    return {
        "ir": "live_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }


def build_live_topology_graph(
    live: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = [{"id": "live:root", "type": "live_runtime"}]
    edges: List[Dict[str, Any]] = []

    db = live.get("database", {})
    if db.get("tables"):
        db_id = f"db:{db.get('database_type', 'db')}"
        nodes.append({"id": db_id, "type": "database"})
        edges.append({"from": "live:root", "to": db_id, "relation": "connects"})

    api = live.get("api", {})
    if api.get("endpoints"):
        api_id = f"api:{api.get('api_type', 'rest')}"
        nodes.append({"id": api_id, "type": "api"})
        edges.append({"from": "live:root", "to": api_id, "relation": "exposes"})

    containers = live.get("containers", {})
    for container in containers.get("containers", [])[:1000]:
        cid = str(container.get("id", container) if isinstance(container, dict) else container)
        nodes.append({"id": f"container:{cid}", "type": "container"})
        edges.append({"from": "live:root", "to": f"container:{cid}", "relation": "runs"})

    k8s = live.get("kubernetes", {})
    for pod in k8s.get("pods", [])[:1000]:
        pid = str(pod.get("name", pod) if isinstance(pod, dict) else pod)
        nodes.append({"id": f"pod:{pid}", "type": "pod"})
        edges.append({"from": "live:root", "to": f"pod:{pid}", "relation": "schedules"})

    return {
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(
            edges,
            key=lambda item: (item.get("from", ""), item.get("to", "")),
        ),
        "bounded": True,
    }
