from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.connectors.api_connector_engine import extract_api_runtime
from core.connectors.cicd_connector_engine import extract_cicd_runtime
from core.connectors.container_connector_engine import extract_container_runtime
from core.connectors.database_connector_engine import extract_database_runtime
from core.connectors.filesystem_connector_engine import extract_filesystem_runtime
from core.connectors.ide_connector_engine import extract_ide_runtime
from core.connectors.kubernetes_connector_engine import extract_kubernetes_runtime
from core.connectors.live_runtime_memory_engine import load_live_runtime
from core.connectors.live_runtime_memory_engine import remember_live_runtime
from core.connectors.live_runtime_memory_engine import save_live_runtime
from core.connectors.runtime_stream_connector_engine import extract_runtime_streams
from core.connectors.telemetry_connector_engine import extract_telemetry_runtime
from core.ir.live_runtime_ir import (
    build_live_topology_graph,
    compile_live_runtime_ir,
    live_runtime_ir_to_graph,
)


def run_live_runtime(
    config: Optional[Dict[str, Any]] = None,
    snapshot: Optional[Dict[str, Any]] = None,
    memory: Optional[Dict[str, Any]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    config = config or {}
    snap = snapshot or {}
    memory = dict(memory or {})

    database = extract_database_runtime(
        config.get("database_type", "postgresql"),
        snap.get("database"),
    )
    api = extract_api_runtime(
        config.get("api_type", "rest"),
        snap.get("api"),
    )
    streams = extract_runtime_streams(
        config.get("stream_types"),
        snap,
    )
    filesystem = extract_filesystem_runtime(
        config.get("filesystem_root", "."),
        snap.get("filesystem"),
    )
    containers = extract_container_runtime(
        config.get("container_runtime", "docker"),
        snap.get("containers"),
    )
    kubernetes = extract_kubernetes_runtime(snap.get("kubernetes"))
    cicd = extract_cicd_runtime(
        config.get("cicd_provider", "github_actions"),
        snap.get("cicd"),
    )
    telemetry = extract_telemetry_runtime(
        config.get("telemetry_backends"),
        snap.get("telemetry"),
    )
    ide = extract_ide_runtime(
        config.get("ide", "vscode"),
        snap.get("ide"),
    )

    payload = {
        "database": database,
        "api": api,
        "streams": streams,
        "filesystem": filesystem,
        "containers": containers,
        "kubernetes": kubernetes,
        "cicd": cicd,
        "telemetry": telemetry,
        "ide": ide,
        "tick": tick,
        "bounded": True,
    }

    graph = build_live_topology_graph(payload)
    payload["graph"] = graph
    payload["sync_state"] = {
        "stream_lineage": streams,
        "topology": graph,
    }

    stream_lineage = []
    for stream in streams.get("streams", []):
        stream_lineage.extend(stream.get("event_lineage", []))

    updated_memory = remember_live_runtime(
        memory,
        {
            "connector_states": {
                "database": database,
                "api": api,
                "containers": containers,
                "kubernetes": kubernetes,
            },
            "stream_states": streams,
            "topology": graph,
            "telemetry_lineage": telemetry.get("distributed_correlations", []),
            "snapshots": payload,
            "stream_lineage": stream_lineage,
        },
    )
    payload["memory"] = updated_memory
    payload["replay"] = {
        "stream_lineage": stream_lineage,
        "topology": graph,
        "replayed": True,
        "bounded": True,
    }
    payload["live_ir"] = compile_live_runtime_ir(payload)
    return payload


def run_live_for_extraction(
    live_runtime: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    config: Optional[Dict[str, Any]] = None,
    snapshot: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not live_runtime:
        return {"enabled": False, "bounded": True}

    memory: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_live_runtime(memory_path, memory_key)
        if loaded.get("available"):
            memory = loaded.get("memory", memory)

    result = run_live_runtime(
        config=config,
        snapshot=snapshot,
        memory=memory,
        tick=tick,
    )

    persisted = False
    if memory_path and memory_key:
        save_live_runtime(memory_path, result.get("memory", {}), memory_key)
        persisted = True

    graph_ir = live_runtime_ir_to_graph(result.get("live_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "live": result,
        "live_ir": result.get("live_ir", {}),
        "live_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "memory_persisted": persisted,
        "bounded": True,
    }
