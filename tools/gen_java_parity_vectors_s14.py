#!/usr/bin/env python3
"""Session-14 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s14.py <out.json>

Covers the dependency-clean core.streaming + core.connectors.live_runtime family:
build_stream_timeline, replay_stream_events, run_live_runtime, save_live_runtime,
load_live_runtime + the live IR and filesystem/cicd sub-engines. Python is the oracle.
Filesystem snapshots are always supplied so the OS-walk fallback is never exercised.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.streaming.stream_replay_engine import build_stream_timeline, replay_stream_events
from core.connectors.live_runtime_orchestrator import run_live_runtime
from core.connectors.live_runtime_memory_engine import (
    save_live_runtime, load_live_runtime, remember_live_runtime)
from core.connectors.filesystem_connector_engine import extract_filesystem_runtime
from core.connectors.cicd_connector_engine import extract_cicd_runtime
from core.connectors.database_connector_engine import extract_database_runtime
from core.connectors.api_connector_engine import extract_api_runtime
from core.connectors.runtime_stream_connector_engine import extract_runtime_streams
from core.connectors.container_connector_engine import extract_container_runtime
from core.connectors.kubernetes_connector_engine import extract_kubernetes_runtime
from core.connectors.telemetry_connector_engine import extract_telemetry_runtime
from core.connectors.ide_connector_engine import extract_ide_runtime
from core.ir.live_runtime_ir import (
    build_live_topology_graph, compile_live_runtime_ir, live_runtime_ir_to_graph)

# NOTE: run_live_runtime is intentionally NOT certified here. Its output is self-referential
# (payload["memory"]["snapshots"] is payload), so stable_serialize recurses infinitely in
# Python itself — it is inherently non-byte-exact-serializable (manifest classification:
# Partial). The Java port is faithful but un-certifiable; see JAVA_SESSION_14_BLOCKER_AUDIT.md.
# Engine vectors below build a NON-cyclic `live` dict directly from the connector engines.

KEY = "live-key-2024"

SNAP = {
    "database": {"tables": [{"name": "users"}], "queries": []},
    "api": {"endpoints": [{"path": "/v1"}]},
    "kafka": {"topics": ["events"]},
    "filesystem": {"root": "/srv", "files": ["b.txt", "a.txt"], "mutations": [{"op": "write"}],
                   "sync": {"state": "ok"}, "permissions": {"a.txt": "rw"}, "inodes": [1, 2]},
    "containers": {"containers": [{"id": "c1"}, {"id": "c2"}]},
    "kubernetes": {"pods": [{"name": "p1"}], "deployments": [{"name": "d1"}]},
    "cicd": {"workflows": [{"id": "wf"}], "jobs": [], "logs": ["l1"], "deployment_graph": {"x": 1}},
    "telemetry": {"traces": []},
    "ide": {"workspace": {"root": "/ws"}},
}

EVENTS = [
    {"id": "s2", "timestamp": 2, "source": "kafka"},
    {"id": "s1", "timestamp": 1, "source": "websocket"},
    {"id": "s3", "timestamp": 1, "source": "redis"},
]


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def _resolve(obj, path):
    cur = obj
    for part in path.split("."):
        cur = cur.get(part, {})
    return cur


def proj(name, inputs, result, paths):
    """Projection-parity entry: each non-cyclic output path is compared to the oracle.

    Used for outputs that are self-referential as a whole (run_live_runtime sets
    payload.memory.snapshots = payload) and therefore not serializable in one shot, but whose
    every computed value IS serializable. Proves byte-exact behavior path-by-path.
    """
    projections = []
    for path in paths:
        value = _resolve(result, path)
        projections.append({"path": path, "serialized": stable_serialize(value),
                            "hash": compute_kaalka_hash(value)})
    return {"name": name, "inputs": inputs, "projections": projections}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 14: streaming + live_runtime family)"}

    out["build_stream_timeline"] = [
        ev("tl_empty", {"events": []}, build_stream_timeline([])),
        ev("tl_null", {}, build_stream_timeline([])),  # absent "events" -> Java null guard
        ev("tl_events", {"events": EVENTS}, build_stream_timeline(EVENTS)),
        ev("tl_unicode", {"events": [{"id": "café", "timestamp": 0, "source": "点"},
                                     {"id": "a", "timestamp": 0, "source": "z"}]},
           build_stream_timeline([{"id": "café", "timestamp": 0, "source": "点"},
                                  {"id": "a", "timestamp": 0, "source": "z"}])),
        # string timestamps exercise the int() coercion arm; missing-id/source defaults too
        ev("tl_string_ts", {"events": [{"id": "x", "timestamp": "3"}, {"id": "y", "timestamp": "1"},
                                       {"timestamp": "1", "source": "s"}]},
           build_stream_timeline([{"id": "x", "timestamp": "3"}, {"id": "y", "timestamp": "1"},
                                  {"timestamp": "1", "source": "s"}])),
        # tied (timestamp,id) different source exercises the tertiary comparator;
        # boolean timestamp exercises the bool() int-coercion arm
        ev("tl_ties", {"events": [{"id": "a", "timestamp": 0, "source": "z"},
                                  {"id": "a", "timestamp": 0, "source": "a"},
                                  {"id": "b", "timestamp": True}]},
           build_stream_timeline([{"id": "a", "timestamp": 0, "source": "z"},
                                  {"id": "a", "timestamp": 0, "source": "a"},
                                  {"id": "b", "timestamp": True}])),
    ]

    out["replay_stream_events"] = [
        ev("replay_empty", {"stream_log": []}, replay_stream_events(None, [])),
        ev("replay_null", {}, replay_stream_events(None, [])),  # absent "stream_log" -> Java null guard
        ev("replay_log", {"stream_log": [{"id": "e1", "payload": "x"}, {"id": "e2"}]},
           replay_stream_events(None, [{"id": "e1", "payload": "x"}, {"id": "e2"}])),
    ]

    # run_live_runtime — projection parity (output is self-referential; compare every value path)
    RUN_PATHS = ["database", "api", "streams", "filesystem", "containers", "kubernetes", "cicd",
                 "telemetry", "ide", "graph", "sync_state", "live_ir", "replay", "tick", "bounded",
                 "memory.connector_states", "memory.stream_states", "memory.topology",
                 "memory.telemetry_lineage", "memory.stream_lineage"]
    run_cfgs = [
        ("run_default", {}, {"filesystem": {"files": []}}, {}, 0),
        ("run_full", {"database_type": "mysql", "api_type": "graphql", "ide": "intellij"}, SNAP, {}, 3),
        ("run_memory", {}, {"filesystem": {"files": ["a"]}}, {"connector_states": {"old": 1}, "extra": 2}, 0),
        ("run_streams", {"stream_types": ["kafka", "redis"]},
         {"kafka": {"topics": ["t1"]}, "redis": {"channels": ["c1"]}, "filesystem": {"files": []}}, {}, 0),
    ]
    out["run_live_runtime"] = []
    for nm, cfg, snap, memv, tick in run_cfgs:
        res = run_live_runtime(config=cfg, snapshot=snap, memory=memv, tick=tick)
        out["run_live_runtime"].append(
            proj(nm, {"config": cfg, "snapshot": snap, "memory": memv, "tick": tick}, res, RUN_PATHS))

    # save/load_live_runtime (real FS)
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s14_")
    mems = [("mem_simple", {"connector_states": {}, "bounded": True}),
            ("mem_unicode", {"note": "café \U0001F600", "用户": 1, "bounded": True}),
            ("mem_nested", {"topology": {"nodes": [{"id": "n"}]}, "stream_states": {"s": 1}})]
    for nm, mem in mems:
        fname = nm + ".json"
        p = os.path.join(d, fname)
        save_live_runtime(p, mem, KEY)
        with open(p, encoding="utf-8") as fh:
            content = fh.read()
        save_vecs.append({"name": nm, "inputs": {"filename": fname, "memory": mem, "key": KEY},
                          "file_content": content})
        load_ret = load_live_runtime(p, KEY)
        load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                          "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    miss = load_live_runtime(os.path.join(d, "nope.json"), KEY)
    load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                      "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
    out["save_live_runtime"] = save_vecs
    out["load_live_runtime"] = load_vecs

    # ---- engine-level parity (Python oracle; inputs carried) ----
    FS = SNAP["filesystem"]
    out["extract_filesystem_runtime"] = [
        ev("fs_snapshot", {"root": ".", "snapshot": FS}, extract_filesystem_runtime(".", FS)),
        ev("fs_empty_snapshot", {"root": "/x", "snapshot": {}}, extract_filesystem_runtime("/x", {})),
        # null-snapshot, missing directory: deterministic + byte-exact (root is the same literal path)
        ev("fs_walk_missing", {"root": "/wwx_nonexistent_dir_zzz", "snapshot": None},
           extract_filesystem_runtime("/wwx_nonexistent_dir_zzz", None)),
    ]
    # null-snapshot FS walk over a real flat temp dir (order-portable). root is env-specific so it
    # is normalized to "<ROOT>" on both sides before comparison (same treatment as save-path).
    fs_files = ["a.txt", "b.txt", "c.txt"]
    fwd = tempfile.mkdtemp(prefix="wwx_s14_fs_")
    for fn in fs_files:
        open(os.path.join(fwd, fn), "w", encoding="utf-8").close()
    fs_walk = dict(extract_filesystem_runtime(fwd, None))
    fs_walk["root"] = "<ROOT>"
    out["extract_filesystem_walk"] = [
        {"name": "walk_flat", "files": fs_files,
         "serialized": stable_serialize(fs_walk), "hash": compute_kaalka_hash(fs_walk)},
    ]
    out["extract_cicd_runtime"] = [
        ev("cicd_default", {"provider": "github_actions", "snapshot": None},
           extract_cicd_runtime("github_actions", None)),
        ev("cicd_full", {"provider": "gitlab", "snapshot": SNAP["cicd"]},
           extract_cicd_runtime("gitlab", SNAP["cicd"])),
    ]
    # build a NON-cyclic `live` dict directly from the connector engines (no orchestrator)
    _streams = extract_runtime_streams(None, SNAP)
    LIVE = {
        "database": extract_database_runtime("mysql", SNAP["database"]),
        "api": extract_api_runtime("rest", SNAP["api"]),
        "streams": _streams,
        "filesystem": extract_filesystem_runtime(".", SNAP["filesystem"]),
        "containers": extract_container_runtime("docker", SNAP["containers"]),
        "kubernetes": extract_kubernetes_runtime(SNAP["kubernetes"]),
        "cicd": extract_cicd_runtime("github_actions", SNAP["cicd"]),
        "telemetry": extract_telemetry_runtime(None, SNAP["telemetry"]),
        "ide": extract_ide_runtime("vscode", SNAP["ide"]),
        "tick": 0, "bounded": True,
    }
    _graph = build_live_topology_graph(LIVE)
    LIVE["graph"] = _graph
    LIVE["sync_state"] = {"stream_lineage": _streams, "topology": _graph}
    out["build_live_topology_graph"] = [
        ev("topo", {"live": LIVE}, build_live_topology_graph(LIVE)),
        ev("topo_empty", {"live": {}}, build_live_topology_graph({})),
        # string containers/pods + no db tables / no api endpoints (defensive arms)
        ev("topo_strings", {"live": {"containers": {"containers": ["c1", "c2"]},
                                     "kubernetes": {"pods": ["p1"]}, "database": {}, "api": {}}},
           build_live_topology_graph({"containers": {"containers": ["c1", "c2"]},
                                      "kubernetes": {"pods": ["p1"]}, "database": {}, "api": {}})),
    ]
    IR = compile_live_runtime_ir(LIVE)
    out["compile_live_runtime_ir"] = [
        ev("ir", {"live": LIVE}, IR),
    ]
    out["live_runtime_ir_to_graph"] = [
        ev("ir2graph", {"live_ir": IR}, live_runtime_ir_to_graph(IR)),
        ev("ir2graph_empty", {"live_ir": {}}, live_runtime_ir_to_graph({})),
        # string deployments + stream with topics + a stream without topics (defensive arms)
        ev("ir2graph_strings", {"live_ir": {"kubernetes": {"deployments": ["d1", "d2"]},
            "stream_lineage": {"streams": [{"stream_type": "kafka", "topics": ["t1"]},
                                           {"stream_type": "redis", "topics": []}]}}},
           live_runtime_ir_to_graph({"kubernetes": {"deployments": ["d1", "d2"]},
            "stream_lineage": {"streams": [{"stream_type": "kafka", "topics": ["t1"]},
                                           {"stream_type": "redis", "topics": []}]}})),
    ]
    out["remember_live_runtime"] = [
        ev("remember", {"memory": {"connector_states": {"a": 1}}, "update": {"topology": {"t": 1}}},
           remember_live_runtime({"connector_states": {"a": 1}}, {"topology": {"t": 1}})),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s14.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
