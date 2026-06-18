#!/usr/bin/env python3
"""Session-13 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s13.py <out.json>

Covers the entire dependency-clean core.causality family + its sub-engines.
Python is the oracle; save/load record file content / recovered output.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.causality.causality_orchestrator import run_causality_runtime, run_causality_for_extraction
from core.causality.causal_replay_engine import replay_causal_runtime
from core.causality.causal_memory_engine import save_causal_memory, load_causal_memory, remember_causal_runtime
from core.causality.runtime_causality_engine import build_runtime_causality
from core.causality.event_chain_engine import build_event_chain
from core.causality.cross_runtime_alignment_engine import align_cross_runtime_events
from core.causality.runtime_dependency_engine import build_runtime_dependencies
from core.causality.workflow_propagation_engine import build_workflow_propagation
from core.causality.causal_graph_engine import build_causal_graph
from core.causality.state_transition_engine import build_state_transitions
from core.causality.runtime_sequence_engine import build_runtime_sequence
from core.causality.runtime_timeline_engine import build_runtime_timeline
from core.causality.runtime_correlation_engine import correlate_runtime_mutations
from core.causality.distributed_causality_engine import build_distributed_causality
from core.causality.browser_native_bridge_engine import bridge_browser_native_runtime
from core.causality.electron_terminal_bridge_engine import bridge_electron_terminal_runtime
from core.causality.notification_causality_engine import track_notification_causality
from core.causality.process_causality_engine import track_process_causality
from core.causality.causal_recovery_engine import recover_causal_runtime

KEY = "caus-key-2024"

EVENTS = [
    {"id": "browser:evt:0", "runtime": "browser", "type": "click", "step": 0},
    {"id": "terminal:evt:1", "runtime": "terminal", "type": "log", "step": 1, "state": "ok"},
    {"id": "desktop:notif:2", "runtime": "desktop", "type": "notification", "step": 2},
]


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 13: causality family)"}

    def rcr(name, **kw):
        return ev(name, kw, run_causality_runtime(**kw))
    out["run_causality_runtime"] = [
        rcr("run_default"),
        rcr("run_interactions", interactions=[{"action": "click", "selector": "#a"},
            {"action": "fill", "from": "#a", "to": "#b", "state": "typed"}]),
        rcr("run_browser_events", browser_events=EVENTS),
        rcr("run_native", native_cognition={"runtime": "desktop", "interactions": [{"action": "focus"}],
            "terminal": {"output": ["line1", "line2"]}, "electron": {"routes": ["/home"]},
            "desktop": {"notifications": [{"id": "n1", "interaction": True}, "plain"]},
            "processes": {"processes": [{"name": "proc1", "parent": "init"}]}}),
        rcr("run_application", application_result={"workflow": {"nodes": [{"n": 1}, {"n": 2}]}},
            interactions=[{"action": "click"}]),
        rcr("run_distributed", distributed_result={"workers": [{"worker_id": "w1"}], "autonomous": True,
            "tasks": [{"t": 1}]}),
        rcr("run_memory", memory={"event_chains": {"old": 1}, "alignment": {"a": 1}}, interactions=[{"action": "x"}]),
        rcr("run_unicode", interactions=[{"action": "点击", "selector": ".café", "state": "\U0001F600"}]),
    ]

    out["replay_causal_runtime"] = [
        ev("replay_empty", {"memory": {}}, replay_causal_runtime({})),
        ev("replay_full", {"memory": {"runtime_propagation": {"p": 1}, "event_chains": {"e": 1},
            "synchronization_state": {"s": 1}, "causal_graphs": {"g": 1}, "alignment": {"al": 1}}},
           replay_causal_runtime({"runtime_propagation": {"p": 1}, "event_chains": {"e": 1},
            "synchronization_state": {"s": 1}, "causal_graphs": {"g": 1}, "alignment": {"al": 1}})),
    ]

    def rfe(name, **kw):
        return ev(name, kw, run_causality_for_extraction(**kw))
    out["run_causality_for_extraction"] = [
        rfe("rfe_disabled", causality_runtime=False),
        rfe("rfe_default"),
        rfe("rfe_no_merge", merge_graph=False),
        rfe("rfe_interactions", interactions=[{"action": "click"}]),
    ]

    # save/load_causal_memory (real FS)
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s13_")
    mems = [("mem_simple", {"event_chains": {}, "bounded": True}),
            ("mem_unicode", {"note": "café \U0001F600", "用户": 1, "bounded": True}),
            ("mem_nested", {"causal_graphs": {"nodes": [{"id": "n"}]}, "alignment": {"a": 1}})]
    for nm, mem in mems:
        fname = nm + ".json"
        p = os.path.join(d, fname)
        save_causal_memory(p, mem, KEY)
        with open(p, encoding="utf-8") as fh:
            content = fh.read()
        save_vecs.append({"name": nm, "inputs": {"filename": fname, "memory": mem, "key": KEY},
                          "file_content": content})
        load_ret = load_causal_memory(p, KEY)
        load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                          "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    miss = load_causal_memory(os.path.join(d, "nope.json"), KEY)
    load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                      "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
    out["save_causal_memory"] = save_vecs
    out["load_causal_memory"] = load_vecs

    # ---- engine-level parity (Python oracle; inputs carried) ----
    CAUS = build_runtime_causality(EVENTS, {"browser": 1})
    out["build_runtime_causality"] = [
        ev("caus_empty", {"events": [], "origins": {}}, build_runtime_causality([], {})),
        ev("caus_events", {"events": EVENTS, "origins": {"browser": 1}}, CAUS),
    ]
    out["build_event_chain"] = [
        ev("chain_empty", {"events": []}, build_event_chain([])),
        ev("chain_events", {"events": EVENTS}, build_event_chain(EVENTS)),
    ]
    ALIGN = align_cross_runtime_events(EVENTS)
    out["align_cross_runtime_events"] = [
        ev("align", {"events": EVENTS}, ALIGN),
        ev("align_unknown", {"events": [{"id": "x", "runtime": "weird", "step": 0},
            {"id": "y", "runtime": "browser", "step": 1}]},
           align_cross_runtime_events([{"id": "x", "runtime": "weird", "step": 0},
            {"id": "y", "runtime": "browser", "step": 1}])),
    ]
    PROP = build_workflow_propagation(ALIGN, {"synchronization_chains": []})
    out["build_runtime_dependencies"] = [
        ev("deps", {"events": EVENTS, "propagation": {"handoffs": [{"from": "a", "to": "b", "workflow_id": "w1"}]}},
           build_runtime_dependencies(EVENTS, {"handoffs": [{"from": "a", "to": "b", "workflow_id": "w1"}]})),
    ]
    out["build_workflow_propagation"] = [
        ev("prop", {"aligned": ALIGN, "dependencies": {"synchronization_chains": [{"s": 1}]}},
           build_workflow_propagation(ALIGN, {"synchronization_chains": [{"s": 1}]})),
    ]
    out["build_causal_graph"] = [
        ev("graph", {"events": EVENTS, "causality": CAUS}, build_causal_graph(EVENTS, CAUS)),
        ev("graph_empty", {"events": [], "causality": {}}, build_causal_graph([], {})),
    ]
    out["build_state_transitions"] = [
        ev("trans", {"events": EVENTS}, build_state_transitions(EVENTS)),
    ]
    out["build_runtime_sequence"] = [
        ev("seq", {"events": EVENTS}, build_runtime_sequence(EVENTS)),
    ]
    out["build_runtime_timeline"] = [
        ev("timeline", {"events": EVENTS, "propagation": PROP}, build_runtime_timeline(EVENTS, PROP)),
    ]
    out["correlate_runtime_mutations"] = [
        ev("corr", {"browser_events": [{"id": "b1"}], "native_events": [{"id": "n1", "runtime": "desktop"}],
                    "notifications": [{"id": "x"}], "terminal_lines": ["l1"], "process_events": [{"name": "p1"}]},
           correlate_runtime_mutations(browser_events=[{"id": "b1"}],
               native_events=[{"id": "n1", "runtime": "desktop"}], notifications=[{"id": "x"}],
               terminal_lines=["l1"], process_events=[{"name": "p1"}])),
    ]
    out["build_distributed_causality"] = [
        ev("dist", {"distributed_result": {"workers": [{"w": 1}], "autonomous": True, "tasks": [{"t": 1}]},
                    "worker_events": [{"worker_id": "w1", "id": "e1"}]},
           build_distributed_causality({"workers": [{"w": 1}], "autonomous": True, "tasks": [{"t": 1}]},
               [{"worker_id": "w1", "id": "e1"}])),
    ]
    out["bridge_browser_native_runtime"] = [
        ev("bridge_bn", {"browser_events": [{"id": "b1"}], "native_events": [{"id": "n1", "runtime": "terminal"}]},
           bridge_browser_native_runtime([{"id": "b1"}], [{"id": "n1", "runtime": "terminal"}])),
        ev("bridge_bn_empty", {"browser_events": [], "native_events": [{"id": "n1"}]},
           bridge_browser_native_runtime([], [{"id": "n1"}])),
    ]
    out["bridge_electron_terminal_runtime"] = [
        ev("bridge_et", {"electron_events": [{"id": "e1"}], "terminal_events": [{"id": "t1"}]},
           bridge_electron_terminal_runtime([{"id": "e1"}], [{"id": "t1"}])),
    ]
    out["track_notification_causality"] = [
        ev("notif", {"notifications": [{"id": "n1", "interaction": True}, "plain"], "origin_events": [{"id": "o1"}]},
           track_notification_causality([{"id": "n1", "interaction": True}, "plain"], [{"id": "o1"}])),
    ]
    out["track_process_causality"] = [
        ev("proc", {"processes": [{"name": "p1", "parent": "init"}, {"pid": 5}], "events": EVENTS},
           track_process_causality([{"name": "p1", "parent": "init"}, {"pid": 5}], EVENTS)),
    ]
    out["recover_causal_runtime"] = [
        ev("recover", {"causality": CAUS, "events": EVENTS}, recover_causal_runtime(CAUS, EVENTS)),
        ev("recover_empty", {"causality": {}, "events": EVENTS}, recover_causal_runtime({}, EVENTS)),
    ]
    out["remember_causal_runtime"] = [
        ev("remember", {"memory": {"event_chains": {"a": 1}}, "update": {"alignment": {"al": 1}}},
           remember_causal_runtime({"event_chains": {"a": 1}}, {"alignment": {"al": 1}})),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s13.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
