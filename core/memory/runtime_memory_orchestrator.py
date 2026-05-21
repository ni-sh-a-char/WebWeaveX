from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.runtime_memory_ir import (
    compile_runtime_memory_ir,
    runtime_memory_ir_to_graph,
)
from core.memory.distributed_memory_engine import build_distributed_memory
from core.memory.knowledge_memory_engine import build_knowledge_memory
from core.memory.runtime_convergence_memory_engine import converge_runtime_memory
from core.memory.runtime_diff_memory_engine import diff_runtime_memory
from core.memory.runtime_federation_engine import federate_runtime_memory
from core.memory.runtime_graph_memory_engine import build_runtime_memory_graph
from core.memory.runtime_history_engine import append_runtime_history
from core.memory.runtime_index_engine import build_runtime_index
from core.memory.runtime_lineage_memory_engine import build_runtime_lineage_memory
from core.memory.runtime_memory_engine import build_runtime_memory
from core.memory.runtime_memory_persistence_engine import load_runtime_memory
from core.memory.runtime_memory_persistence_engine import save_runtime_memory
from core.memory.runtime_memory_policy_engine import build_runtime_memory_policy
from core.memory.runtime_memory_policy_engine import enforce_memory_policy
from core.memory.runtime_merge_engine import merge_runtime_memories
from core.memory.runtime_query_engine import query_runtime_memory
from core.memory.runtime_replication_engine import replicate_runtime_memory
from core.memory.runtime_search_engine import search_runtime_memory
from core.memory.runtime_snapshot_memory_engine import capture_memory_snapshot
from core.memory.semantic_memory_engine import build_semantic_memory


def _collect_history(
    sources: Dict[str, Any],
    tick: int,
) -> List[Dict[str, Any]]:
    history: List[Dict[str, Any]] = []

    if sources.get("workflow"):
        history.append({"tick": tick, "kind": "workflow", "source": "workflow"})
    if sources.get("sync"):
        history.append({"tick": tick, "kind": "sync", "source": "sync"})
    if sources.get("evolution"):
        history.append({"tick": tick, "kind": "evolution", "source": "evolution"})
    if sources.get("live"):
        history.append({"tick": tick, "kind": "live", "source": "connectors"})
    if sources.get("extraction"):
        history.append({"tick": tick, "kind": "extraction", "source": "browser"})

    return history


def run_runtime_memory(
    sources: Optional[Dict[str, Any]] = None,
    stored: Optional[Dict[str, Any]] = None,
    nodes: Optional[List[Dict[str, Any]]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    sources = sources or {}
    stored = dict(stored or {})
    nodes = list(nodes or [{"node_id": "primary", "synced": True}])

    prior_runtime = stored.get("runtime", {})
    history = list(prior_runtime.get("runtime_history", []))
    for entry in _collect_history(sources, tick):
        history = append_runtime_history(history, entry)

    entities = []
    relations = []
    semantic_src = sources.get("semantic", {})
    if semantic_src:
        inner = semantic_src.get("semantic", semantic_src)
        entities = inner.get("entities", {}).get("entities", [])
        relations = inner.get("entities", {}).get("relations", [])

    knowledge = build_knowledge_memory(
        entities=entities,
        relations=relations,
        topology={
            "graphs": [sources.get("graph", {})],
            "distributed": sources.get("distributed", {}),
            "application": sources.get("application", {}),
        },
    )
    semantic = build_semantic_memory(semantic_src, history)

    lineage = build_runtime_lineage_memory(
        selector=sources.get("evolution", {}).get("selector", {}).get("selectors", []),
        workflow=[{"id": "wf:0", "ancestor": ""}],
        sync=sources.get("sync", {}).get("lineage", []),
        evolution=sources.get("evolution", {}).get("lineage", []),
        extraction=[{"id": f"extract:{tick}", "ancestor": ""}],
    )

    runtime = build_runtime_memory(
        runtime_history=history,
        lineage=lineage.get("lineage", []),
        semantic_relations=knowledge.get("semantic_relations", []),
    )

    graph = build_runtime_memory_graph(
        knowledge.get("entities", []),
        knowledge.get("semantic_relations", []),
    )

    index = build_runtime_index(
        entities=knowledge.get("entities", []),
        workflows=[{"id": sources.get("workflow", {}).get("objective", "operate")}],
        graphs=[graph],
        streams=list(sources.get("live", {}).get("streams", {}).get("streams", [])),
        connectors=[sources.get("live", {})],
    )

    replication = replicate_runtime_memory(runtime, nodes)
    convergence = converge_runtime_memory(replication.get("replicas", []))
    distributed = build_distributed_memory(nodes)

    federated = federate_runtime_memory([runtime, prior_runtime] if prior_runtime else [runtime])
    merged = merge_runtime_memories([runtime, prior_runtime] if prior_runtime else [runtime])

    policy = build_runtime_memory_policy()
    enforcement = enforce_memory_policy(
        policy,
        runtime.get("runtime_history", []),
        runtime.get("lineage", []),
        replication.get("replica_count", 0),
    )

    diff = diff_runtime_memory(prior_runtime, runtime) if prior_runtime else {"revertible": True}
    snapshot = capture_memory_snapshot(
        {
            "runtime": runtime,
            "knowledge": knowledge,
            "graph": graph,
        },
        tick=tick,
    )

    payload = {
        "runtime": runtime,
        "knowledge": knowledge,
        "semantic": semantic,
        "lineage": lineage,
        "graph": graph,
        "index": index,
        "distributed": distributed,
        "federation": federated,
        "merged": merged,
        "replication": replication,
        "convergence": convergence,
        "policy": policy,
        "enforcement": enforcement,
        "diff": diff,
        "snapshot": snapshot,
        "bounded": True,
    }

    payload["replay"] = {
        "lineage": lineage.get("lineage", []),
        "runtime_history": runtime.get("runtime_history", []),
        "memory_id": runtime.get("memory_id", ""),
        "replayed": True,
        "bounded": True,
    }
    payload["memory_ir"] = compile_runtime_memory_ir(payload)
    return payload


def run_memory_for_extraction(
    federated_memory: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    sources: Optional[Dict[str, Any]] = None,
    nodes: Optional[List[Dict[str, Any]]] = None,
    tick: int = 0,
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not federated_memory:
        return {"enabled": False, "bounded": True}

    stored: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_runtime_memory(memory_path, memory_key)
        if loaded.get("available"):
            stored = loaded.get("memory", stored)

    result = run_runtime_memory(
        sources=sources,
        stored=stored,
        nodes=nodes,
        tick=tick,
    )

    store = {
        "runtime": result.get("runtime", {}),
        "knowledge": result.get("knowledge", {}),
        "semantic": result.get("semantic", {}),
        "index": result.get("index", {}),
        "graph": result.get("graph", {}),
        "lineage": result.get("lineage", {}),
        "snapshot": result.get("snapshot", {}),
        "bounded": True,
    }

    persisted = False
    if memory_path and memory_key:
        save_runtime_memory(memory_path, store, memory_key)
        persisted = True

    graph_ir = runtime_memory_ir_to_graph(result.get("memory_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "memory": result,
        "memory_ir": result.get("memory_ir", {}),
        "memory_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "query": query_runtime_memory(result.get("runtime", {}), "semantic", ""),
        "search": search_runtime_memory(result.get("index", {}), ""),
        "memory_persisted": persisted,
        "bounded": True,
    }
