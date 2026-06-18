#!/usr/bin/env python3
"""Session-10 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s10.py <out.json>

Covers the entire dependency-clean core.synchronization family + its sub-engines.
Each entry stores inputs + stable_serialize + compute_kaalka_hash of the Python output;
save/load_sync_memory record the written file content (Python-traceable).
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.synchronization.runtime_delta_engine import build_runtime_delta
from core.synchronization.runtime_replay_engine import replay_synchronized_runtime
from core.synchronization.runtime_sync_orchestrator import (
    run_synchronized_runtime, run_sync_for_extraction,
)
from core.synchronization.runtime_sync_memory_engine import (
    save_sync_memory, load_sync_memory, remember_sync_runtime,
)
from core.synchronization.runtime_snapshot_engine import capture_runtime_snapshot
from core.synchronization.runtime_drift_engine import detect_runtime_drift
from core.synchronization.runtime_diff_engine import diff_runtime_state
from core.synchronization.runtime_mutation_engine import track_runtime_mutations
from core.synchronization.runtime_merge_engine import merge_runtime_realities
from core.synchronization.runtime_convergence_engine import converge_runtime_state
from core.synchronization.runtime_sync_engine import synchronize_runtime
from core.synchronization.reality_replication_engine import replicate_runtime_reality
from core.synchronization.runtime_federation_engine import federate_runtime_realities
from core.synchronization.runtime_alignment_engine import align_runtime_layers
from core.synchronization.runtime_continuity_engine import maintain_runtime_continuity
from core.synchronization.runtime_history_engine import build_runtime_history
from core.synchronization.runtime_timeline_engine import build_sync_timeline
from core.synchronization.runtime_state_graph_engine import build_runtime_state_graph
from core.synchronization.runtime_consistency_engine import verify_runtime_consistency

KEY = "sync-key-2024"


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 10: synchronization family)"}

    VIEW_A = {"dom": {"a": 1}, "semantic": {"s": 1}, "workflow": {"w": 1}, "runtime": {"r": 1}}
    VIEW_B = {"dom": {"a": 2}, "semantic": {"s": 1}, "workflow": {"w": 2}, "state": {"x": 1}}

    out["build_runtime_delta"] = [
        ev("delta_empty", {"previous": {}, "current": {}}, build_runtime_delta({}, {}, tick=0)),
        ev("delta_changes", {"previous": VIEW_A, "current": VIEW_B}, build_runtime_delta(VIEW_A, VIEW_B, tick=3)),
        ev("delta_add", {"previous": {}, "current": {"dom": {"x": 1}, "semantic_k": {}}},
           build_runtime_delta({}, {"dom": {"x": 1}, "semantic_k": {}}, tick=1)),
        ev("delta_unicode", {"previous": {"用户": "a"}, "current": {"用户": "b", "工作流workflow": 1}},
           build_runtime_delta({"用户": "a"}, {"用户": "b", "工作流workflow": 1}, tick=0)),
        ev("delta_nested_eq", {"previous": {"k": {"n": [1, 2]}}, "current": {"k": {"n": [1, 2]}}},
           build_runtime_delta({"k": {"n": [1, 2]}}, {"k": {"n": [1, 2]}}, tick=0)),
    ]

    MEM = {"history": {"h": 1}, "deltas": [{"delta_id": "d1"}], "timeline": {"t": 1},
           "realities": [{"reality_id": "primary"}], "convergence": {"converged": True}}
    out["replay_synchronized_runtime"] = [
        ev("replay_empty", {"memory": {}}, replay_synchronized_runtime({})),
        ev("replay_full", {"memory": MEM}, replay_synchronized_runtime(MEM)),
    ]

    def rsr(name, **kw):
        return ev(name, kw, run_synchronized_runtime(**kw))

    out["run_synchronized_runtime"] = [
        rsr("rsr_default"),
        rsr("rsr_views", browser={"dom": {"a": 1}, "runtime": {"r": 1}},
            semantic_result={"semantic": {"s": 1}}, workflow_result={"workflow": {"w": 1}}, tick=2),
        rsr("rsr_distributed", browser={"dom": {"a": 1}},
            distributed_result={"workers": [{"worker_id": "w2"}, {"worker_id": "w1"}]}, tick=1),
        rsr("rsr_memory", browser={"dom": {"a": 2}},
            memory={"last_view": {"dom": {"a": 1}}, "deltas": [{"delta_id": "old", "timestamp": 0}]}, tick=5),
        rsr("rsr_session", browser={"dom": {"a": 1}}, session={"sid": "x"}, identity={"id": "y"},
            native={"n": 1}, tick=3),
    ]

    def rfe(name, **kw):
        return ev(name, kw, run_sync_for_extraction(**kw))

    out["run_sync_for_extraction"] = [
        rfe("rfe_disabled", synchronized_runtime=False),
        rfe("rfe_default"),
        rfe("rfe_no_merge", merge_graph=False),
        rfe("rfe_views", browser={"dom": {"a": 1}, "runtime": {"r": 1}}, workflow_result={"workflow": {"w": 1}}),
    ]

    # save/load_sync_memory (real FS in temp dir; file content + load output recorded)
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s10_")
    mems = [("mem_simple", {"deltas": [], "history": {"h": 1}, "bounded": True}),
            ("mem_unicode", {"note": "café \U0001F600", "用户": 1, "bounded": True}),
            ("mem_nested", {"realities": [{"reality_id": "p", "tick": 1}], "convergence": {"converged": True}})]
    for nm, mem in mems:
        fname = nm + ".json"
        p = os.path.join(d, fname)
        save_sync_memory(p, mem, KEY)
        with open(p, encoding="utf-8") as fh:
            content = fh.read()
        save_vecs.append({"name": nm, "inputs": {"filename": fname, "memory": mem, "key": KEY},
                          "file_content": content})
        load_ret = load_sync_memory(p, KEY)
        load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                          "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    miss = load_sync_memory(os.path.join(d, "nope.json"), KEY)
    load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                      "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
    out["save_sync_memory"] = save_vecs
    out["load_sync_memory"] = load_vecs

    # ---- engine-level parity (covers internal branches; Python oracle; inputs carried) ----
    def snap(name, **kw):
        return ev(name, kw, capture_runtime_snapshot(**kw))
    out["capture_runtime_snapshot"] = [
        snap("snap_empty", tick=0),
        snap("snap_full", browser={"b": 1}, native={"n": 1}, semantic={"s": 1}, workflow={"w": 1},
             causality={"c": 1}, sync_state={"y": 1}, tick=2),
    ]
    out["detect_runtime_drift"] = [
        ev("drift_none", {"baseline": {"selectors": {"a": 1}}, "current": {"selectors": {"a": 1}}},
           detect_runtime_drift({"selectors": {"a": 1}}, {"selectors": {"a": 1}})),
        ev("drift_some", {"baseline": {"selectors": {"a": 1}, "semantic": {}},
                          "current": {"selectors": {"a": 2}, "runtime": {"r": 1}}},
           detect_runtime_drift({"selectors": {"a": 1}, "semantic": {}}, {"selectors": {"a": 2}, "runtime": {"r": 1}})),
    ]
    out["diff_runtime_state"] = [
        ev("diff_mixed", {"previous": {"semantic_x": 1, "workflow_y": 1, "worker_z": 1, "other": 1},
                          "current": {"semantic_x": 2, "workflow_y": 2, "worker_z": 2, "other": 2}},
           diff_runtime_state({"semantic_x": 1, "workflow_y": 1, "worker_z": 1, "other": 1},
                              {"semantic_x": 2, "workflow_y": 2, "worker_z": 2, "other": 2})),
    ]
    out["track_runtime_mutations"] = [
        ev("tm_sync", {"changes": [{"field": "z"}, {"field": "a"}], "tick": 4},
           track_runtime_mutations([{"field": "z"}, {"field": "a"}], tick=4)),
    ]
    MR = [{"reality_id": "b", "tick": 2, "semantic": {"s": 1}, "workflow": {"w": 1}, "application": {"a": 1}},
          {"reality_id": "a", "tick": 1, "semantic": {"s2": 2}}]
    out["merge_runtime_realities"] = [ev("merge", {"realities": MR}, merge_runtime_realities(MR))]
    CR = [{"reality_id": "b", "k": 1}, {"reality_id": "a", "k": 2, "j": 3}]
    out["converge_runtime_state"] = [ev("converge", {"realities": CR}, converge_runtime_state(CR))]
    out["synchronize_runtime"] = [
        ev("sync_empty", {"snapshots": [], "tick": 0}, synchronize_runtime([], tick=0)),
        ev("sync_snap", {"snapshots": [{"browser_runtime": {"u": "x"}, "native_runtime": {"n": 1}}], "tick": 1},
           synchronize_runtime([{"browser_runtime": {"u": "x"}, "native_runtime": {"n": 1}}], tick=1)),
    ]
    out["replicate_runtime_reality"] = [
        ev("repl_empty", {"source": {"reality_id": "p"}, "workers": []},
           replicate_runtime_reality({"reality_id": "p"}, [])),
        ev("repl_workers", {"source": {"reality_id": "p", "semantic_state": {"s": 1}},
                            "workers": [{"worker_id": "w1"}, {"id": "w2"}]},
           replicate_runtime_reality({"reality_id": "p", "semantic_state": {"s": 1}},
                                     [{"worker_id": "w1"}, {"id": "w2"}])),
    ]
    out["federate_runtime_realities"] = [
        ev("fed_empty", {}, federate_runtime_realities()),
        ev("fed_full", {"workers": [{"worker_id": "w1"}], "browser": {"b": 1}, "native": {"n": 1},
                        "semantic": {"s": 1}, "application": {"a": 1}},
           federate_runtime_realities(workers=[{"worker_id": "w1"}], browser={"b": 1}, native={"n": 1},
                                      semantic={"s": 1}, application={"a": 1})),
    ]
    out["align_runtime_layers"] = [
        ev("align_none", {}, align_runtime_layers()),
        ev("align_some", {"browser": {"b": 1}, "semantic": {"s": 1}},
           align_runtime_layers(browser={"b": 1}, semantic={"s": 1})),
    ]
    out["maintain_runtime_continuity"] = [
        ev("cont_empty", {}, maintain_runtime_continuity()),
        ev("cont_full", {"session": {"s": 1}, "identity": {"i": 1}, "workflow": {"w": 1},
                         "semantic": {"m": 1}, "checkpoint": {"c": 1}},
           maintain_runtime_continuity(session={"s": 1}, identity={"i": 1}, workflow={"w": 1},
                                       semantic={"m": 1}, checkpoint={"c": 1})),
    ]
    D = [{"delta_id": "d2", "timestamp": 2, "changes": [{"field": "f1", "kind": "semantic_change"}]},
         {"delta_id": "d1", "timestamp": 1, "changes": [{"field": "f2", "kind": "ui_mutation"}]}]
    hist = build_runtime_history(D, workflows=[{"w": 1}])
    out["build_runtime_history"] = [
        ev("hist_empty", {"deltas": []}, build_runtime_history([])),
        ev("hist_deltas", {"deltas": D, "workflows": [{"w": 1}]}, hist),
    ]
    out["build_sync_timeline"] = [ev("timeline", {"history": hist}, build_sync_timeline(hist))]
    out["build_runtime_state_graph"] = [
        ev("sg_empty", {"snapshot": {}, "delta": {}, "convergence": {}}, build_runtime_state_graph({}, {}, {})),
        ev("sg_changes", {"snapshot": {"snapshot_id": "snapshot:1"},
                          "delta": {"delta_id": "d1", "changes": [{"field": "f1"}, {"field": "f2"}]},
                          "convergence": {"converged": True}},
           build_runtime_state_graph({"snapshot_id": "snapshot:1"},
               {"delta_id": "d1", "changes": [{"field": "f1"}, {"field": "f2"}]}, {"converged": True})),
    ]
    out["verify_runtime_consistency"] = [
        ev("cons_ok", {"history": hist, "convergence": {"converged": True}, "replay": {"replayed": True}},
           verify_runtime_consistency(hist, {"converged": True}, {"replayed": True})),
        ev("cons_issues", {"history": {"deltas": []}, "convergence": {"converged": False},
                           "replay": {"replayed": False}},
           verify_runtime_consistency({"deltas": []}, {"converged": False}, {"replayed": False})),
    ]
    out["remember_sync_runtime"] = [
        ev("remember", {"memory": {"deltas": [1]}, "update": {"history": {"h": 1}, "last_view": {"v": 1}}},
           remember_sync_runtime({"deltas": [1]}, {"history": {"h": 1}, "last_view": {"v": 1}})),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s10.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
