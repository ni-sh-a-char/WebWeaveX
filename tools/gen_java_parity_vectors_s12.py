#!/usr/bin/env python3
"""Session-12 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s12.py <out.json>

Covers the entire dependency-clean core.evolution_runtime family + its sub-engines.
Python is the oracle; save/load record file content / recovered output.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.evolution_runtime.runtime_evolution_engine import build_runtime_evolution
from core.evolution_runtime.selector_evolution_engine import evolve_selector_runtime
from core.evolution_runtime.runtime_evolution_orchestrator import (
    run_evolution_runtime, run_evolution_for_extraction)
from core.evolution_runtime.runtime_memory_engine import (
    save_evolution_runtime, load_evolution_runtime, remember_evolution_runtime)
from core.evolution_runtime.workflow_evolution_engine import evolve_workflow_runtime
from core.evolution_runtime.semantic_evolution_engine import evolve_semantic_runtime
from core.evolution_runtime.topology_evolution_engine import evolve_runtime_topology
from core.evolution_runtime.runtime_strategy_engine import build_runtime_strategy
from core.evolution_runtime.runtime_repair_engine import repair_runtime_failures
from core.evolution_runtime.runtime_recovery_evolution_engine import evolve_recovery_order
from core.evolution_runtime.runtime_optimization_engine import optimize_runtime_execution
from core.evolution_runtime.runtime_adaptation_engine import adapt_runtime_strategy
from core.evolution_runtime.runtime_mutation_engine import build_runtime_mutations
from core.evolution_runtime.runtime_lineage_engine import build_runtime_lineage
from core.evolution_runtime.runtime_policy_engine import build_runtime_policy, enforce_runtime_policy
from core.evolution_runtime.runtime_pattern_engine import build_runtime_patterns
from core.evolution_runtime.runtime_convergence_engine import converge_runtime_evolution
from core.evolution_runtime.runtime_diff_engine import diff_evolution_runtime
from core.evolution_runtime.runtime_evolution_graph_engine import build_runtime_evolution_graph

KEY = "evo-key-2024"


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 12: evolution_runtime family)"}

    MUT = [{"kind": "selector", "target": "#z"}, {"kind": "workflow", "target": "execution_ordering"},
           {"kind": "selector", "target": "#a"}]
    LIN = [{"id": "b1"}, {"id": "a1"}]
    out["build_runtime_evolution"] = [
        ev("evo_empty", {"mutations": [], "lineage": []}, build_runtime_evolution([], [])),
        ev("evo_mutations", {"mutations": MUT, "lineage": LIN}, build_runtime_evolution(MUT, LIN)),
    ]

    def sel(name, **kw):
        return ev(name, kw, evolve_selector_runtime(**kw))
    out["evolve_selector_runtime"] = [
        sel("sel_empty"),
        sel("sel_healed", selectors={"#a": ".a2", "#b": ".b2"}, healed={"#a": ".healed-a"}),
        sel("sel_unicode", selectors={"按钮": ".btn"}, healed={"café": ".c2"}),
    ]

    def rer(name, **kw):
        return ev(name, kw, run_evolution_runtime(**kw))
    out["run_evolution_runtime"] = [
        rer("run_default"),
        rer("run_workflow", workflow_result={"workflow": {"plan": {"steps": [{"id": "s1", "priority": 1},
            {"id": "s2", "priority": 0}]}, "execution": {"executed": [{"step_id": "s1"}]}}}),
        rer("run_semantic", semantic_result={"semantic": {"entities": {"entities": [{"label": "User"},
            {"label": "Account"}, {"type": "Order"}]}, "domain": {"domain": "saas"}, "ontology": {"o": 1}}}),
        rer("run_failures", failures=["broken_selector", "failed_workflow", "failed_workflow", "sync_divergence"]),
        rer("run_distributed", distributed_result={"workers": [{"worker_id": "w2"}, {"worker_id": "w1"}]}),
        rer("run_sync", sync_result={"synchronization": {"drift": {"drifts": [{"d": 1}]},
            "deltas": [{"x": 1}], "convergence": {"converged": True}}}),
        rer("run_memory", memory={"last_evolution_id": "prev123", "last_evolution": {"evolution_id": "prev123",
            "mutations": []}, "evolution_histories": [{"evolution_id": "h1"}]}),
        rer("run_adaptive", adaptive_memory={"selectors": {"#x": ".x2"}, "healed_selectors": {"#y": ".healed-y"}}),
    ]

    def rfe(name, **kw):
        return ev(name, kw, run_evolution_for_extraction(**kw))
    out["run_evolution_for_extraction"] = [
        rfe("rfe_disabled", evolving_runtime=False),
        rfe("rfe_default"),
        rfe("rfe_no_merge", merge_graph=False),
        rfe("rfe_failures", failures=["broken_selector"]),
    ]

    # save/load_evolution_runtime (real FS)
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s12_")
    mems = [("mem_simple", {"evolution_histories": [], "bounded": True}),
            ("mem_unicode", {"note": "café \U0001F600", "用户": 1, "bounded": True}),
            ("mem_nested", {"selector_lineage": [{"id": "a"}], "last_evolution_id": "x"})]
    for nm, mem in mems:
        fname = nm + ".json"
        p = os.path.join(d, fname)
        save_evolution_runtime(p, mem, KEY)
        with open(p, encoding="utf-8") as fh:
            content = fh.read()
        save_vecs.append({"name": nm, "inputs": {"filename": fname, "memory": mem, "key": KEY},
                          "file_content": content})
        load_ret = load_evolution_runtime(p, KEY)
        load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                          "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    miss = load_evolution_runtime(os.path.join(d, "nope.json"), KEY)
    load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                      "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
    out["save_evolution_runtime"] = save_vecs
    out["load_evolution_runtime"] = load_vecs

    # ---- engine-level parity (Python oracle; inputs carried) ----
    PLAN = {"steps": [{"id": "s2", "priority": 0}, {"id": "s1", "priority": 1}]}
    EXEC = {"executed": [{"step_id": "s1"}, {"step_id": "s2"}]}
    out["evolve_workflow_runtime"] = [
        ev("wf", {"plan": PLAN, "execution": EXEC, "history": [{"h": 1}]},
           evolve_workflow_runtime(PLAN, EXEC, [{"h": 1}])),
    ]
    SEM = {"semantic": {"entities": {"entities": [{"label": "A"}, {"type": "B"}, {"label": "A"}]},
           "ontology": {"o": 1}, "domain": {"domain": "saas"}}}
    out["evolve_semantic_runtime"] = [
        ev("sem_empty", {"semantic": {}, "history": []}, evolve_semantic_runtime({}, [])),
        ev("sem_full", {"semantic": SEM, "history": [{"h": 1}]}, evolve_semantic_runtime(SEM, [{"h": 1}])),
    ]
    out["evolve_runtime_topology"] = [
        ev("topo", {"workers": [{"worker_id": "w2"}, {"id": "w1"}], "sync": {}, "causality": {"c": 1}},
           evolve_runtime_topology([{"worker_id": "w2"}, {"id": "w1"}], {}, {"c": 1})),
    ]
    out["build_runtime_strategy"] = [
        ev("strat_clean", {"evidence": {"drift_count": 0, "failed_steps": 0}},
           build_runtime_strategy({"drift_count": 0, "failed_steps": 0})),
        ev("strat_drift", {"evidence": {"drift_count": 3, "failed_steps": 2}},
           build_runtime_strategy({"drift_count": 3, "failed_steps": 2})),
    ]
    out["repair_runtime_failures"] = [
        ev("repair", {"failures": ["sync_divergence", "broken_selector", "unknown"], "selectors": {"#a": ".a2"}},
           repair_runtime_failures(["sync_divergence", "broken_selector", "unknown"], {"#a": ".a2"})),
    ]
    REP = repair_runtime_failures(["sync_divergence", "broken_selector"], {})
    out["evolve_recovery_order"] = [
        ev("recovery", {"repairs": REP["repairs"]}, evolve_recovery_order(REP["repairs"])),
    ]
    out["optimize_runtime_execution"] = [
        ev("opt_zero", {"depth": 0, "replay_cost": 0, "sync_overhead": 0},
           optimize_runtime_execution(0, 0, 0)),
        ev("opt_vals", {"depth": 150, "replay_cost": 3, "sync_overhead": 2},
           optimize_runtime_execution(150, 3, 2)),
    ]
    STRAT = build_runtime_strategy({"drift_count": 0})
    OPT = optimize_runtime_execution(5, 0, 0)
    out["adapt_runtime_strategy"] = [
        ev("adapt", {"strategy": STRAT, "optimization": OPT}, adapt_runtime_strategy(STRAT, OPT)),
        ev("adapt_pressure", {"strategy": STRAT, "optimization": optimize_runtime_execution(150, 0, 0)},
           adapt_runtime_strategy(STRAT, optimize_runtime_execution(150, 0, 0))),
    ]
    SELR = evolve_selector_runtime({"#a": ".a2"}, {"#b": ".healed-b"})
    WFR = evolve_workflow_runtime(PLAN, EXEC, [])
    SEMR = evolve_semantic_runtime(SEM, [])
    MUTS = build_runtime_mutations(SELR, WFR, SEMR, {"convergence": {"c": 1}})
    out["build_runtime_mutations"] = [
        ev("muts", {"selector": SELR, "workflow": WFR, "semantic": SEMR, "sync": {"convergence": {"c": 1}}}, {"mutations": MUTS}),
    ]
    out["build_runtime_lineage"] = [
        ev("lin_parent", {"evolution_id": "e1", "mutations": MUTS, "parent_id": "p1"},
           {"lineage": build_runtime_lineage("e1", MUTS, "p1")}),
        ev("lin_noparent", {"evolution_id": "e1", "mutations": MUTS, "parent_id": ""},
           {"lineage": build_runtime_lineage("e1", MUTS, "")}),
    ]
    POL = build_runtime_policy()
    out["build_runtime_policy"] = [ev("policy", {}, POL)]
    out["enforce_runtime_policy"] = [
        ev("enforce", {"policy": POL, "mutations": MUTS, "repairs": REP["repairs"], "depth": 5},
           enforce_runtime_policy(POL, MUTS, REP["repairs"], 5)),
    ]
    out["build_runtime_patterns"] = [
        ev("patterns", {"ui": {"z": 1, "a": 1}, "workflows": [{"objective": "extract"}], "semantic": {"s": 1},
                        "sync_history": [{"h": 1}]},
           build_runtime_patterns(ui={"z": 1, "a": 1}, workflows=[{"objective": "extract"}],
               semantic={"s": 1}, sync_history=[{"h": 1}])),
    ]
    EVO1 = build_runtime_evolution(MUTS, [])
    EVO2 = build_runtime_evolution([{"kind": "sync", "target": "convergence"}], [])
    out["converge_runtime_evolution"] = [
        ev("converge", {"evolutions": [EVO1, EVO2]}, converge_runtime_evolution([EVO1, EVO2])),
    ]
    out["diff_evolution_runtime"] = [
        ev("diff", {"previous": EVO2, "current": EVO1}, diff_evolution_runtime(EVO2, EVO1)),
    ]
    out["build_runtime_evolution_graph"] = [
        ev("graph", {"evolution": EVO1, "repairs": REP, "optimization": OPT},
           build_runtime_evolution_graph(EVO1, REP, OPT)),
    ]
    out["remember_evolution_runtime"] = [
        ev("remember", {"memory": {"evolution_histories": [1]}, "update": {"last_evolution_id": "x"}},
           remember_evolution_runtime({"evolution_histories": [1]}, {"last_evolution_id": "x"})),
    ]

    # extra coverage vectors (branch reach): distributed_evolutions extend + [-10:] slice,
    # null-semantic patterns, "type"-fallback entities.
    out["run_evolution_runtime"].append(
        rer("run_dist_memory", memory={"distributed_evolutions": [{"evolution_id": f"d{i}"} for i in range(12)],
            "last_evolution": {"evolution_id": "prev", "mutations": [{"kind": "x", "target": "t"}]}},
            failures=["failed_workflow"]))
    out["build_runtime_patterns"].append(
        ev("patterns_no_semantic", {"ui": {}, "workflows": [{"action": "a"}], "semantic": None, "sync_history": []},
           build_runtime_patterns(ui={}, workflows=[{"action": "a"}], semantic=None, sync_history=[])))
    out["evolve_semantic_runtime"].append(
        ev("sem_type", {"semantic": {"entities": {"entities": [{"type": "T1"}, {"type": "T2"}]}}, "history": []},
           evolve_semantic_runtime({"entities": {"entities": [{"type": "T1"}, {"type": "T2"}]}}, [])))

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s12.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
