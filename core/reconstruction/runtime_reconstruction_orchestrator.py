from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.reconstruction_runtime_ir import (
    compile_reconstruction_runtime_ir,
    reconstruction_runtime_ir_to_graph,
)
from core.reconstruction.application_reconstruction_engine import reconstruct_application_runtime
from core.reconstruction.browser_reconstruction_engine import reconstruct_browser_runtime
from core.reconstruction.runtime_clone_engine import clone_runtime_environment
from core.reconstruction.runtime_connector_reconstruction import reconstruct_connector_runtime
from core.reconstruction.runtime_environment_engine import build_runtime_environment
from core.reconstruction.runtime_fabrication_engine import fabricate_runtime_reality
from core.reconstruction.runtime_identity_reconstruction import reconstruct_runtime_identity
from core.reconstruction.runtime_memory_reconstruction import reconstruct_runtime_memory
from core.reconstruction.runtime_recovery_reconstruction import recover_reconstructed_runtime
from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
from core.reconstruction.runtime_replay_builder import build_runtime_replay
from core.reconstruction.runtime_snapshot_engine import (
    capture_reconstruction_snapshot,
    load_reconstruction_snapshot,
    save_reconstruction_snapshot,
)
from core.reconstruction.runtime_state_rebuilder import rebuild_runtime_state
from core.reconstruction.runtime_timeline_engine import build_runtime_timeline
from core.reconstruction.runtime_topology_reconstruction import reconstruct_runtime_topology
from core.reconstruction.runtime_validation_engine import validate_reconstructed_runtime
from core.reconstruction.session_reconstruction_engine import reconstruct_runtime_session


def run_reconstruction_runtime(
    sources: Optional[Dict[str, Any]] = None,
    stored: Optional[Dict[str, Any]] = None,
    runtime_graph: Optional[Dict[str, Any]] = None,
    runtime_type: str = "browser",
    tick: int = 0,
    fabricate: bool = False,
    clone: bool = False,
) -> Dict[str, Any]:
    sources = sources or {}
    stored = dict(stored or {})
    runtime_graph = runtime_graph or sources.get("graph", {})

    semantic_ir = sources.get("semantic_ir", sources.get("semantic", {}))
    workflow_ir = sources.get("workflow_ir", sources.get("workflow", {}))
    sync_ir = sources.get("sync_ir", sources.get("sync", {}))
    execution_ir = sources.get("execution_ir", sources.get("execution", {}))
    memory_ir = sources.get("memory_ir", sources.get("memory", {}))

    runtime = reconstruct_runtime(
        semantic_ir=semantic_ir,
        workflow_ir=workflow_ir,
        synchronization_ir=sync_ir,
        execution_ir=execution_ir,
        memory_ir=memory_ir,
        runtime_graph=runtime_graph,
        runtime_type=runtime_type,
        tick=tick,
    )

    browser = reconstruct_browser_runtime(
        browser_ir=sources.get("browser_ir", sources.get("browser", {})),
        interaction_ir=sources.get("interaction_ir", {}),
        identity=sources.get("identity", {}),
        session=sources.get("session", {}),
        streaming=sources.get("streaming", sources.get("live", {})),
        dom=sources.get("dom", {}),
    )

    application = reconstruct_application_runtime(
        application_ir=sources.get("application_ir", sources.get("application", {})),
        workflow_ir=workflow_ir,
        execution_ir=execution_ir,
        runtime_type=runtime_type,
    )

    session = reconstruct_runtime_session(
        session=sources.get("session", {}),
        identity=sources.get("identity", {}),
        sync_state=sync_ir,
        adaptive_memory=sources.get("adaptive_memory", {}),
    )

    environment = build_runtime_environment(
        runtime=runtime_type,
        connectors=sources.get("connectors", []),
        workers=sources.get("workers", []),
    )

    memory_rebuilt = reconstruct_runtime_memory(
        memory_ir=memory_ir,
        semantic=semantic_ir,
        lineage=sources.get("lineage", memory_ir.get("lineage", {})),
    )

    state = rebuild_runtime_state(
        queues=execution_ir.get("queues", {}).get("queue", []) if isinstance(execution_ir.get("queues"), dict) else [],
        synchronization=sync_ir,
        mutations=execution_ir.get("mutations", {}).get("mutations", []) if isinstance(execution_ir.get("mutations"), dict) else [],
        transactions=execution_ir.get("transactions", []),
        memory=memory_rebuilt,
        execution_lineage=sources.get("lineage", {}).get("lineage", []) if isinstance(sources.get("lineage"), dict) else [],
        workflows=application.get("workflows", []),
    )

    topology = reconstruct_runtime_topology(
        runtime_graph=runtime_graph,
        workers=sources.get("workers", execution_ir.get("federation", {}).get("workers", [])),
        connectors=sources.get("connectors", []),
        execution_topology=execution_ir.get("federation", {}),
        sync_topology=sync_ir,
    )

    identity = reconstruct_runtime_identity(
        browser_identity=sources.get("identity", {}),
        session=sources.get("session", {}),
        runtime_id=runtime.get("runtime_id", ""),
        execution_id=str(execution_ir.get("transactions", [{}])[0].get("transaction_id", "") if execution_ir.get("transactions") else ""),
        worker_id=str((sources.get("workers") or [{}])[0].get("worker_id", "")),
    )

    connectors = reconstruct_connector_runtime(
        connectors=sources.get("connectors", []),
        live_ir=sources.get("live", sources.get("live_ir", {})),
    )

    actions = execution_ir.get("actions", [])
    timeline = build_runtime_timeline(
        actions=actions,
        mutations=state.get("mutations", []),
        synchronization=[{"id": f"sync:{i}", "tick": tick} for i, _ in enumerate(sync_ir.get("lineage", [])[:100])] if isinstance(sync_ir, dict) else [],
        execution=actions,
        tick=tick,
    )

    replay = build_runtime_replay(
        actions=actions,
        transactions=execution_ir.get("transactions", []),
        timeline=timeline,
        tick=tick,
    )

    clone_result = {}
    if clone:
        source_body = {
            "runtime_graph": runtime_graph,
            "browser": browser,
            "application": application,
            "synchronization": sync_ir,
            "workflows": application.get("workflows", []),
            "queues": state.get("queues", []),
        }
        clone_result = clone_runtime_environment(source_body)

    fabrication = {}
    if fabricate:
        fabrication = fabricate_runtime_reality(
            runtime=runtime,
            environment=environment,
            browser=browser,
            application=application,
        )

    validation = validate_reconstructed_runtime(
        runtime=runtime if not fabricate else fabrication.get("runtime", runtime),
        replay=replay,
        topology=topology,
        execution=execution_ir,
        mutations=state.get("mutations"),
    )

    prior_snapshot = stored.get("snapshot", {})
    recovery = recover_reconstructed_runtime(checkpoint=prior_snapshot)

    snapshot = capture_reconstruction_snapshot({
        "runtime": runtime,
        "browser": browser,
        "application": application,
        "topology": topology,
        "identities": identity,
        "workflows": application.get("workflows", []),
        "replay_chains": replay.get("replay_chains", []),
        "state": state,
    })

    payload = {
        "runtime": runtime,
        "browser": browser,
        "application": application,
        "session": session,
        "environment": environment,
        "memory": memory_rebuilt,
        "state": state,
        "topology": topology,
        "identity": identity,
        "connectors": connectors,
        "timeline": timeline,
        "replay": replay,
        "clone": clone_result,
        "fabrication": fabrication,
        "validation": validation,
        "recovery": recovery,
        "snapshot": snapshot,
        "bounded": True,
    }
    payload["reconstruction_ir"] = compile_reconstruction_runtime_ir(payload)
    return payload


def run_reconstruction_for_extraction(
    reconstruction_runtime: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    sources: Optional[Dict[str, Any]] = None,
    runtime_graph: Optional[Dict[str, Any]] = None,
    runtime_type: str = "browser",
    tick: int = 0,
    fabricate_runtime: bool = False,
    clone_runtime: bool = False,
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not reconstruction_runtime:
        return {"enabled": False, "bounded": True}

    stored: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_reconstruction_snapshot(memory_path, memory_key)
        if loaded.get("available"):
            stored = loaded.get("snapshot", stored)

    result = run_reconstruction_runtime(
        sources=sources,
        stored=stored,
        runtime_graph=runtime_graph,
        runtime_type=runtime_type,
        tick=tick,
        fabricate=fabricate_runtime,
        clone=clone_runtime,
    )

    store = capture_reconstruction_snapshot({
        "runtime": result.get("runtime", {}),
        "topology": result.get("topology", {}),
        "identities": result.get("identity", {}),
        "workflows": result.get("application", {}).get("workflows", []),
        "replay_chains": result.get("replay", {}).get("replay_chains", []),
        "state": result.get("state", {}),
    })

    persisted = False
    if memory_path and memory_key:
        save_reconstruction_snapshot(memory_path, store, memory_key)
        persisted = True

    graph_ir = reconstruction_runtime_ir_to_graph(result.get("reconstruction_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "reconstruction": result,
        "reconstruction_ir": result.get("reconstruction_ir", {}),
        "reconstruction_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "validation": result.get("validation", {}),
        "reconstruction_persisted": persisted,
        "bounded": True,
    }
