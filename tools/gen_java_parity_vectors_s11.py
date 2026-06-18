#!/usr/bin/env python3
"""Session-11 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s11.py <out.json>

Covers the entire dependency-clean core.workflows family + its sub-engines.
Python is the oracle; save/load record file content / recovered output.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.workflows.objective_engine import build_runtime_objective
from core.workflows.workflow_planner_engine import build_workflow_plan
from core.workflows.workflow_replay_engine import replay_workflow_runtime
from core.workflows.workflow_orchestrator import run_autonomous_workflow, run_workflow_for_extraction
from core.workflows.workflow_memory_engine import save_workflow_memory, load_workflow_memory, remember_workflow_runtime
from core.workflows.workflow_execution_engine import execute_workflow_plan
from core.workflows.workflow_state_engine import build_workflow_state
from core.workflows.workflow_navigation_engine import navigate_runtime_workflow
from core.workflows.workflow_transition_engine import build_workflow_transitions
from core.workflows.workflow_dependency_engine import build_workflow_dependencies
from core.workflows.workflow_recovery_engine import recover_workflow_runtime
from core.workflows.workflow_alignment_engine import align_workflow_runtime
from core.workflows.workflow_semantic_alignment_engine import align_workflow_semantics
from core.workflows.workflow_federation_engine import federate_workflow_runtime
from core.workflows.workflow_scheduler_engine import schedule_workflow_execution
from core.workflows.workflow_runtime_engine import build_workflow_runtime_context
from core.workflows.workflow_graph_engine import build_workflow_graph

KEY = "wf-key-2024"


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 11: workflows family)"}

    out["build_runtime_objective"] = [
        ev("obj_dashboard", {"objective": "extract_dashboard", "priority": 0},
           build_runtime_objective("extract_dashboard", 0)),
        ev("obj_unknown", {"objective": "custom_thing", "priority": 5},
           build_runtime_objective("custom_thing", 5)),
        ev("obj_repo", {"objective": "extract_repository", "priority": 2},
           build_runtime_objective("extract_repository", 2)),
        ev("obj_terminal", {"objective": "capture_terminal", "priority": 0},
           build_runtime_objective("capture_terminal", 0)),
    ]

    def plan(name, **kw):
        return ev(name, kw, build_workflow_plan(**kw))
    out["build_workflow_plan"] = [
        plan("plan_default", objective="extract_dashboard"),
        plan("plan_repo", objective="extract_repository"),
        plan("plan_domain", objective="monitor_infrastructure",
             semantic_runtime={"domain": {"domain": "infrastructure"}}),
        plan("plan_application", objective="extract_dashboard",
             application_runtime={"workflow": {"edges": [{"relation": "click"}, {"relation": "fill"}]}}),
        plan("plan_causality", objective="extract_dashboard",
             causality={"causality": {"propagation": {"handoffs": [{"to": "native"}, {"to": "terminal"}]}}}),
    ]

    MEM = {"objectives": {"objective": "x"}, "execution_graphs": {"e": 1},
           "runtime_transitions": [{"from": "a", "to": "b"}], "workflow_states": {"s": 1}}
    out["replay_workflow_runtime"] = [
        ev("replay_empty", {"memory": {}}, replay_workflow_runtime({})),
        ev("replay_full", {"memory": MEM}, replay_workflow_runtime(MEM)),
    ]

    def raw(name, **kw):
        return ev(name, kw, run_autonomous_workflow(**kw))
    out["run_autonomous_workflow"] = [
        raw("run_default"),
        raw("run_priority", objective="extract_invoices", priority=3, tick=2),
        raw("run_application", objective="extract_dashboard",
            application_result={"workflow": {"edges": [{"relation": "click"}]}}),
        raw("run_distributed", objective="monitor_metrics",
            distributed_result={"workers": [{"worker_id": "w2"}, {"worker_id": "w1"}]}),
        raw("run_failures", objective="extract_dashboard", failures=["selector_drift", "modal_interruption"]),
        raw("run_url_unicode", objective="extract_repository", url="https://例.com/path"),
        raw("run_semantic", objective="extract_dashboard",
            semantic_runtime={"semantic": {"domain": {"domain": "saas"}, "ontology": {"o": 1}}}),
    ]

    def rfe(name, **kw):
        return ev(name, kw, run_workflow_for_extraction(**kw))
    out["run_workflow_for_extraction"] = [
        rfe("rfe_disabled", autonomous_workflow=False),
        rfe("rfe_default"),
        rfe("rfe_no_merge", merge_graph=False),
        rfe("rfe_repo", objective="extract_repository", url="https://x.io"),
    ]

    # save/load_workflow_memory (real FS in temp dir)
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s11_")
    mems = [("mem_simple", {"objectives": {"o": 1}, "bounded": True}),
            ("mem_unicode", {"note": "café \U0001F600", "用户": 1, "bounded": True}),
            ("mem_nested", {"workflow_states": {"s": {"deep": [1, 2]}}, "runtime_transitions": []})]
    for nm, mem in mems:
        fname = nm + ".json"
        p = os.path.join(d, fname)
        save_workflow_memory(p, mem, KEY)
        with open(p, encoding="utf-8") as fh:
            content = fh.read()
        save_vecs.append({"name": nm, "inputs": {"filename": fname, "memory": mem, "key": KEY},
                          "file_content": content})
        load_ret = load_workflow_memory(p, KEY)
        load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                          "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    miss = load_workflow_memory(os.path.join(d, "nope.json"), KEY)
    load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                      "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
    out["save_workflow_memory"] = save_vecs
    out["load_workflow_memory"] = load_vecs

    # ---- engine-level parity (Python oracle; inputs carried) ----
    PLAN = build_workflow_plan("extract_dashboard")
    EXEC = execute_workflow_plan(PLAN, tick=1)
    STATE = build_workflow_state(PLAN, EXEC)
    out["execute_workflow_plan"] = [
        ev("exec_empty", {"plan": {"steps": []}, "tick": 0}, execute_workflow_plan({"steps": []}, tick=0)),
        ev("exec_plan", {"plan": PLAN, "tick": 1}, EXEC),
    ]
    out["build_workflow_state"] = [
        ev("state", {"plan": PLAN, "execution": EXEC}, STATE),
    ]
    out["navigate_runtime_workflow"] = [
        ev("nav", {"plan": PLAN, "tick": 2}, navigate_runtime_workflow(PLAN, tick=2)),
        ev("nav_terminal", {"plan": build_workflow_plan("capture_terminal"), "tick": 0},
           navigate_runtime_workflow(build_workflow_plan("capture_terminal"), tick=0)),
    ]
    out["build_workflow_transitions"] = [
        ev("trans", {"execution": EXEC}, {"transitions": build_workflow_transitions(EXEC)}),
    ]
    out["build_workflow_dependencies"] = [
        ev("deps", {"plan": PLAN}, build_workflow_dependencies(PLAN)),
    ]
    out["recover_workflow_runtime"] = [
        ev("rec_failures", {"state": STATE, "failures": ["selector_drift", "worker_failure", "unknown_thing"]},
           recover_workflow_runtime(STATE, ["selector_drift", "worker_failure", "unknown_thing"])),
        ev("rec_implicit", {"state": {"current_step": 2, "retries": 1}, "failures": None},
           recover_workflow_runtime({"current_step": 2, "retries": 1}, None)),
        ev("rec_none", {"state": {"current_step": 0}, "failures": None},
           recover_workflow_runtime({"current_step": 0}, None)),
    ]
    out["align_workflow_runtime"] = [
        ev("align", {"plan": PLAN, "state": STATE, "execution": EXEC}, align_workflow_runtime(PLAN, STATE, EXEC)),
    ]
    out["align_workflow_semantics"] = [
        ev("sem_empty", {"plan": PLAN}, align_workflow_semantics(PLAN)),
        ev("sem_full", {"plan": PLAN, "semantic_runtime": {"semantic": {"ontology": {"o": 1},
                        "domain": {"d": 1}, "semantic_graph": {"g": 1}}},
                        "causality": {"causality": {"propagation": {"h": 1}}}},
           align_workflow_semantics(PLAN, semantic_runtime={"semantic": {"ontology": {"o": 1},
               "domain": {"d": 1}, "semantic_graph": {"g": 1}}},
               causality={"causality": {"propagation": {"h": 1}}})),
    ]
    out["federate_workflow_runtime"] = [
        ev("fed_empty", {}, federate_workflow_runtime()),
        ev("fed_full", {"browser": {"url": "x"}, "native": {"n": 1}, "distributed": {"d": 1},
                        "semantic": {"semantic": {"memory": {"m": 1}}}, "workers": [{"worker_id": "w1"}, {"id": "w2"}]},
           federate_workflow_runtime(browser={"url": "x"}, native={"n": 1}, distributed={"d": 1},
               semantic={"semantic": {"memory": {"m": 1}}}, workers=[{"worker_id": "w1"}, {"id": "w2"}])),
    ]
    out["schedule_workflow_execution"] = [
        ev("sched_empty", {"plans": [], "tick": 0}, schedule_workflow_execution([], tick=0)),
        ev("sched_order", {"plans": [{"objective": "b", "priority": 1}, {"objective": "a", "priority": 1},
                                     {"objective": "c", "priority": 0}], "tick": 0},
           schedule_workflow_execution([{"objective": "b", "priority": 1}, {"objective": "a", "priority": 1},
                                        {"objective": "c", "priority": 0}], tick=0)),
    ]
    out["build_workflow_runtime_context"] = [
        ev("ctx", {"url": "https://x", "runtime": "browser",
                   "sources": {"semantic": True, "causality": False, "application": True}},
           build_workflow_runtime_context("https://x", runtime="browser",
               sources={"semantic": True, "causality": False, "application": True})),
    ]
    OBJ = build_runtime_objective("extract_dashboard", 0)
    TRANS = build_workflow_transitions(EXEC)
    out["build_workflow_graph"] = [
        ev("graph", {"objective": OBJ, "plan": PLAN, "state": STATE, "execution": EXEC, "transitions": TRANS},
           build_workflow_graph(OBJ, PLAN, STATE, EXEC, TRANS)),
        ev("graph_retries", {"objective": OBJ, "plan": PLAN, "state": {"retries": 2}, "execution": EXEC,
                             "transitions": TRANS},
           build_workflow_graph(OBJ, PLAN, {"retries": 2}, EXEC, TRANS)),
    ]
    out["remember_workflow_runtime"] = [
        ev("remember", {"memory": {"objectives": {"o": 1}}, "update": {"workflow_states": {"s": 1}}},
           remember_workflow_runtime({"objectives": {"o": 1}}, {"workflow_states": {"s": 1}})),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s11.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
