#!/usr/bin/env python3
"""Session-16 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s16.py <out.json>

Covers the dependency-clean core.reconstruction orchestrator (run_reconstruction_runtime,
run_reconstruction_for_extraction) + its ~14 sub-engines + IR + snapshot persistence.
Python is the oracle.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.reconstruction.runtime_reconstruction_orchestrator import (
    run_reconstruction_runtime, run_reconstruction_for_extraction)
from core.reconstruction.application_reconstruction_engine import reconstruct_application_runtime
from core.reconstruction.runtime_environment_engine import build_runtime_environment
from core.reconstruction.session_reconstruction_engine import reconstruct_runtime_session
from core.reconstruction.runtime_identity_reconstruction import reconstruct_runtime_identity
from core.reconstruction.runtime_topology_reconstruction import reconstruct_runtime_topology
from core.reconstruction.runtime_connector_reconstruction import reconstruct_connector_runtime
from core.reconstruction.runtime_recovery_reconstruction import recover_reconstructed_runtime
from core.reconstruction.runtime_timeline_engine import build_runtime_timeline
from core.reconstruction.runtime_replay_builder import build_runtime_replay
from core.reconstruction.runtime_state_rebuilder import rebuild_runtime_state
from core.reconstruction.runtime_clone_engine import clone_runtime_environment
from core.reconstruction.runtime_fabrication_engine import fabricate_runtime_reality
from core.reconstruction.runtime_snapshot_engine import (
    capture_reconstruction_snapshot, restore_reconstruction_snapshot,
    save_reconstruction_snapshot, load_reconstruction_snapshot)
from core.ir.reconstruction_runtime_ir import (
    compile_reconstruction_runtime_ir, reconstruction_runtime_ir_to_graph)

KEY = "recon-key-2024"

SOURCES = {
    "semantic_ir": {"ontology": {"entities": ["User"]}, "domain": {"domain": "saas"}},
    "workflow_ir": {"workflows": [{"id": "wf1", "objective": "extract"}], "workflow": {}},
    "sync_ir": {"lineage": [{"id": "l1"}, {"id": "l2"}], "deltas": []},
    "execution_ir": {"actions": [{"id": "a2"}, {"id": "a1"}],
                     "transactions": [{"transaction_id": "tx1"}],
                     "queues": {"queue": [{"priority": 1, "order": 0}, {"priority": 2, "order": 1}]},
                     "mutations": {"mutations": [{"tick": 1, "ordered_index": 0, "kind": "dom"}]},
                     "federation": {"workers": [{"worker_id": "w1"}]}},
    "memory_ir": {"entries": [{"k": "v"}], "lineage": {"lineage": [{"id": "m1"}]}},
    "browser_ir": {"url": "https://x", "dom": {}},
    "identity": {"identity_id": "id1", "fingerprint": "fp"},
    "session": {"authenticated": True, "session_id": "s1", "cookies": [{"name": "b"}, {"name": "a"}],
                "csrf": {"token": "t"}},
    "connectors": [{"id": "c2", "kind": "database"}, {"id": "c1", "kind": "weird"}],
    "workers": [{"worker_id": "w2"}, {"worker_id": "w1"}],
    "dom": {"html": "<div></div>"},
    "live": {"streams": [{"stream_type": "kafka"}]},
    "graph": {"nodes": [{"id": "n2", "type": "x"}, {"id": "n1"}], "edges": [{"from": "n1", "to": "n2"}]},
}


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 16: reconstruction orchestrator)"}

    def rrr(name, **kw):
        return ev(name, kw, run_reconstruction_runtime(**kw))
    out["run_reconstruction_runtime"] = [
        rrr("run_empty"),
        rrr("run_full", sources=SOURCES, tick=2),
        rrr("run_fabricate", sources=SOURCES, fabricate=True, tick=1),
        rrr("run_clone", sources=SOURCES, clone=True),
        rrr("run_both", sources=SOURCES, fabricate=True, clone=True, runtime_type="terminal"),
    ]

    def rfe(name, **kw):
        return ev(name, kw, run_reconstruction_for_extraction(**kw))
    out["run_reconstruction_for_extraction"] = [
        rfe("rfe_disabled", reconstruction_runtime=False),
        rfe("rfe_default", sources=SOURCES),
        rfe("rfe_no_merge", sources=SOURCES, merge_graph=False),
        rfe("rfe_fabricate", sources=SOURCES, fabricate_runtime=True, clone_runtime=True),
    ]

    # ---- engine-level parity ----
    out["reconstruct_application_runtime"] = [
        ev("app", {"application_ir": {"forms": {"f": 1}, "dashboards": ["d"]},
                   "workflow_ir": SOURCES["workflow_ir"], "execution_ir": {"state": {"s": 1}},
                   "runtime_type": "browser"},
           reconstruct_application_runtime({"forms": {"f": 1}, "dashboards": ["d"]},
               SOURCES["workflow_ir"], {"state": {"s": 1}}, "browser")),
        ev("app_dict_wf", {"application_ir": {}, "workflow_ir": {"workflow": {"objective": "x"}},
                           "execution_ir": {}, "runtime_type": "vm"},
           reconstruct_application_runtime({}, {"workflow": {"objective": "x"}}, {}, "vm")),
    ]
    out["build_runtime_environment"] = [
        ev("env", {"runtime": "terminal", "connectors": [{"id": "c2"}, {"id": "c1"}], "workers": [{"worker_id": "w1"}]},
           build_runtime_environment("terminal", [{"id": "c2"}, {"id": "c1"}], [{"worker_id": "w1"}])),
        ev("env_invalid", {"runtime": "nope", "connectors": [], "workers": []},
           build_runtime_environment("nope", [], [])),
    ]
    out["reconstruct_runtime_session"] = [
        ev("session", {"session": SOURCES["session"], "identity": SOURCES["identity"],
                       "sync_state": {"s": 1}, "adaptive_memory": {"a": 1}},
           reconstruct_runtime_session(SOURCES["session"], SOURCES["identity"], {"s": 1}, {"a": 1})),
    ]
    out["reconstruct_runtime_identity"] = [
        ev("identity", {"browser_identity": {"b": 1}, "session": {"s": 1}, "runtime_id": "r1",
                        "execution_id": "e1", "worker_id": "w1"},
           reconstruct_runtime_identity({"b": 1}, {"s": 1}, "r1", "e1", "w1")),
    ]
    out["reconstruct_runtime_topology"] = [
        ev("topology", {"runtime_graph": SOURCES["graph"], "workers": SOURCES["workers"],
                        "connectors": SOURCES["connectors"], "execution_topology": {"e": 1}, "sync_topology": {"s": 1}},
           reconstruct_runtime_topology(SOURCES["graph"], SOURCES["workers"], SOURCES["connectors"],
               {"e": 1}, {"s": 1})),
    ]
    out["reconstruct_connector_runtime"] = [
        ev("connectors", {"connectors": SOURCES["connectors"], "live_ir": SOURCES["live"]},
           reconstruct_connector_runtime(SOURCES["connectors"], SOURCES["live"])),
        ev("connectors_dict_streams", {"connectors": [], "live_ir": {"streams": {"streams": [{"x": 1}]}}},
           reconstruct_connector_runtime([], {"streams": {"streams": [{"x": 1}]}})),
    ]
    out["recover_reconstructed_runtime"] = [
        ev("recover", {"checkpoint": {"snap": 1}, "failed_segments": [{"id": "s2"}, {"id": "s1"}]},
           recover_reconstructed_runtime({"snap": 1}, [{"id": "s2"}, {"id": "s1"}])),
        ev("recover_empty", {"checkpoint": {}, "failed_segments": []},
           recover_reconstructed_runtime({}, [])),
    ]
    ACTIONS = [{"id": "a2"}, {"id": "a1"}]
    out["build_runtime_timeline"] = [
        ev("timeline", {"actions": ACTIONS, "mutations": [{"id": "m1", "tick": 0}], "execution": ACTIONS, "tick": 1},
           build_runtime_timeline(actions=ACTIONS, mutations=[{"id": "m1", "tick": 0}], execution=ACTIONS, tick=1)),
    ]
    TL = build_runtime_timeline(actions=ACTIONS, tick=0)
    out["build_runtime_replay"] = [
        ev("replay", {"actions": ACTIONS, "transactions": [{"transaction_id": "tx1"}], "timeline": TL, "tick": 1},
           build_runtime_replay(ACTIONS, [{"transaction_id": "tx1"}], TL, 1)),
    ]
    out["rebuild_runtime_state"] = [
        ev("state", {"queues": [{"priority": 1, "order": 0}, {"priority": 2, "order": 1}],
                     "synchronization": {"s": 1}, "mutations": [{"tick": 1, "ordered_index": 0, "kind": "dom"}],
                     "transactions": [{"transaction_id": "tx1"}], "memory": {"m": 1},
                     "execution_lineage": [{"id": "l1"}], "workflows": [{"id": "wf1"}]},
           rebuild_runtime_state([{"priority": 1, "order": 0}, {"priority": 2, "order": 1}], {"s": 1},
               [{"tick": 1, "ordered_index": 0, "kind": "dom"}], [{"transaction_id": "tx1"}], {"m": 1},
               [{"id": "l1"}], [{"id": "wf1"}])),
    ]
    out["clone_runtime_environment"] = [
        ev("clone", {"source": {"runtime_graph": SOURCES["graph"], "browser": {"b": 1},
                                "application": {"a": 1}, "workflows": [{"id": "wf"}], "queues": [{"q": 1}]}},
           clone_runtime_environment({"runtime_graph": SOURCES["graph"], "browser": {"b": 1},
                                      "application": {"a": 1}, "workflows": [{"id": "wf"}], "queues": [{"q": 1}]})),
    ]
    out["fabricate_runtime_reality"] = [
        ev("fabricate", {"runtime": {"runtime_id": "r1", "x": 1}, "environment": {"runtime": "vm"},
                         "browser": {"b": 1}, "application": {"a": 1}},
           fabricate_runtime_reality({"runtime_id": "r1", "x": 1}, {"runtime": "vm"}, {"b": 1}, {"a": 1})),
    ]
    out["capture_reconstruction_snapshot"] = [
        ev("capture", {"state": {"topology": {"t": 1}, "identities": {"i": 1}, "workflows": [{"w": 1}],
                                 "replay_chains": [{"c": 1}], "extra": 9}},
           capture_reconstruction_snapshot({"topology": {"t": 1}, "identities": {"i": 1},
               "workflows": [{"w": 1}], "replay_chains": [{"c": 1}], "extra": 9})),
    ]
    out["restore_reconstruction_snapshot"] = [
        ev("restore", {"snapshot": {"state": {"topology": {"t": 1}}, "workflows": [{"w": 1}]}},
           restore_reconstruction_snapshot({"state": {"topology": {"t": 1}}, "workflows": [{"w": 1}]})),
    ]
    PAYLOAD = run_reconstruction_runtime(sources=SOURCES, fabricate=True, clone=True)
    IR = compile_reconstruction_runtime_ir(PAYLOAD)
    out["compile_reconstruction_runtime_ir"] = [ev("ir", {"payload": PAYLOAD}, IR)]
    out["reconstruction_runtime_ir_to_graph"] = [
        ev("ir2graph", {"ir": IR}, reconstruction_runtime_ir_to_graph(IR)),
        ev("ir2graph_empty", {"ir": {}}, reconstruction_runtime_ir_to_graph({})),
    ]

    # ---- extra coverage vectors (comparator tiers / defensive arms) ----
    out["rebuild_runtime_state"].append(
        ev("state_rich", {"queues": [{"priority": 1, "order": 1}, {"priority": 1, "order": 0}],
                          "synchronization": {}, "mutations": [{"tick": 1, "ordered_index": 1, "kind": "b"},
                          {"tick": 1, "ordered_index": 1, "kind": "a"}, {"tick": 0, "ordered_index": 0, "kind": "z"}],
                          "transactions": [{"transaction_id": "t2"}, {"transaction_id": "t1"}],
                          "memory": {}, "execution_lineage": [{"id": "l2"}, {"id": "l1"}],
                          "workflows": [{"objective": "o2"}, {"id": "w1"}]},
           rebuild_runtime_state([{"priority": 1, "order": 1}, {"priority": 1, "order": 0}], {},
               [{"tick": 1, "ordered_index": 1, "kind": "b"}, {"tick": 1, "ordered_index": 1, "kind": "a"},
                {"tick": 0, "ordered_index": 0, "kind": "z"}], [{"transaction_id": "t2"}, {"transaction_id": "t1"}],
               {}, [{"id": "l2"}, {"id": "l1"}], [{"objective": "o2"}, {"id": "w1"}])))
    out["fabricate_runtime_reality"].append(
        ev("fabricate_none", {"runtime": None, "environment": {"runtime": "vm"}, "browser": {}, "application": {}},
           fabricate_runtime_reality(None, {"runtime": "vm"}, {}, {})))
    out["reconstruct_runtime_topology"].append(
        ev("topology_edges", {"runtime_graph": {"nodes": [{"id": "n1"}], "edges": [
            {"from": "a", "to": "b", "relation": "z"}, {"from": "a", "to": "b", "relation": "a"},
            {"from": "a", "to": "a", "relation": "x"}]}, "workers": [{"worker_id": "w2"}, {"worker_id": "w1"}],
            "connectors": [{"id": "c2"}, {"id": "c1"}], "execution_topology": {}, "sync_topology": {}},
           reconstruct_runtime_topology({"nodes": [{"id": "n1"}], "edges": [
            {"from": "a", "to": "b", "relation": "z"}, {"from": "a", "to": "b", "relation": "a"},
            {"from": "a", "to": "a", "relation": "x"}]}, [{"worker_id": "w2"}, {"worker_id": "w1"}],
            [{"id": "c2"}, {"id": "c1"}], {}, {})))
    out["build_runtime_replay"].append(
        ev("replay_actionid", {"actions": [{"action_id": "a2"}, {"action_id": "a1"}], "transactions": [],
                               "timeline": None, "tick": 0},
           build_runtime_replay([{"action_id": "a2"}, {"action_id": "a1"}], [], None, 0)))
    out["build_runtime_environment"].append(
        ev("env_electron", {"runtime": "electron", "connectors": [{"id": "c1"}], "workers": [{"worker_id": "w1"}]},
           build_runtime_environment("electron", [{"id": "c1"}], [{"worker_id": "w1"}])))
    out["build_runtime_timeline"].append(
        ev("timeline_coerce", {"actions": [{"id": "x", "tick": "5"}, {"id": "y", "tick": True}], "tick": 0},
           build_runtime_timeline(actions=[{"id": "x", "tick": "5"}, {"id": "y", "tick": True}], tick=0)))

    # save/load_reconstruction_snapshot (real FS)
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s16_")
    snaps = [("snap_simple", {"state": {}, "bounded": True}),
             ("snap_unicode", {"note": "café \U0001F600", "用户": 1, "bounded": True}),
             ("snap_nested", capture_reconstruction_snapshot({"topology": {"t": 1}, "workflows": [{"w": 1}]}))]
    for nm, snap in snaps:
        fname = nm + ".json"
        p = os.path.join(d, fname)
        save_reconstruction_snapshot(p, snap, KEY)
        with open(p, encoding="utf-8") as fh:
            content = fh.read()
        save_vecs.append({"name": nm, "inputs": {"filename": fname, "snapshot": snap, "key": KEY},
                          "file_content": content})
        load_ret = load_reconstruction_snapshot(p, KEY)
        load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                          "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    miss = load_reconstruction_snapshot(os.path.join(d, "nope.json"), KEY)
    load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                      "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
    out["save_reconstruction_snapshot"] = save_vecs
    out["load_reconstruction_snapshot"] = load_vecs

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s16.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
