#!/usr/bin/env python3
"""Session-9 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s9.py <out.json>

Covers the entire dependency-clean core.execution family:
build_runtime_sandbox / execute_runtime_action / replay_runtime_execution /
simulate_runtime_execution / run_execution_runtime / run_execution_for_extraction.
Each entry stores inputs + stable_serialize + compute_kaalka_hash of the Python output.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.execution.runtime_sandbox_engine import build_runtime_sandbox
from core.execution.runtime_execution_engine import execute_runtime_action
from core.execution.runtime_replay_engine import replay_runtime_execution
from core.execution.runtime_simulation_engine import simulate_runtime_execution
from core.execution.runtime_execution_orchestrator import (
    run_execution_runtime, run_execution_for_extraction,
)
from core.execution.runtime_permissions_engine import build_runtime_permissions
from core.execution.runtime_policy_engine import build_runtime_policy


def e(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 9: execution family)"}

    # build_runtime_sandbox
    out["build_runtime_sandbox"] = [
        e("sb_browser", {"runtime": "browser"}, build_runtime_sandbox("browser")),
        e("sb_terminal", {"runtime": "terminal"}, build_runtime_sandbox("terminal")),
        e("sb_native", {"runtime": "native"}, build_runtime_sandbox("native")),
        e("sb_vm", {"runtime": "vm"}, build_runtime_sandbox("vm")),
        e("sb_unknown", {"runtime": "exotic"}, build_runtime_sandbox("exotic")),
        e("sb_custom_allowed", {"runtime": "browser", "allowed_actions": ["zeta", "alpha", "Mu"]},
          build_runtime_sandbox("browser", allowed_actions=["zeta", "alpha", "Mu"])),
        e("sb_custom_params",
          {"runtime": "browser", "rollback_enabled": False, "max_actions": 50,
           "timeout_ticks": 200, "replay_policy": "lenient"},
          build_runtime_sandbox("browser", rollback_enabled=False, max_actions=50,
                                timeout_ticks=200, replay_policy="lenient")),
        e("sb_unicode_allowed", {"runtime": "browser", "allowed_actions": ["按钮", "a", "\U0001F600"]},
          build_runtime_sandbox("browser", allowed_actions=["按钮", "a", "\U0001F600"])),
    ]

    # execute_runtime_action (sandbox/policy/permissions recorded explicitly)
    sb = build_runtime_sandbox("browser")
    sb_term = build_runtime_sandbox("terminal")
    sb_native = build_runtime_sandbox("native")
    perms_browser = build_runtime_permissions(["browser", "native", "terminal", "connector", "vm"])
    perms_none = build_runtime_permissions(["filesystem"])
    pol = build_runtime_policy()

    def ea(name, raw, sandbox, policy=None, permissions=None, tick=0):
        return e(name, {"raw_action": raw, "sandbox": sandbox, "policy": policy,
                        "permissions": permissions, "tick": tick},
                 execute_runtime_action(raw, sandbox=sandbox, policy=policy,
                                        permissions=permissions, tick=tick))

    out["execute_runtime_action"] = [
        ea("ea_click_ok", {"type": "browser_click", "selector": "#submit"}, sb, pol, perms_browser),
        ea("ea_no_selector", {"type": "browser_click", "selector": ""}, sb, pol, perms_browser),
        ea("ea_terminal_safe", {"type": "terminal_command", "command": "pwd"}, sb_term, build_runtime_policy(True),
           build_runtime_permissions(["terminal"])),
        ea("ea_terminal_unsafe", {"type": "terminal_command", "command": "rm -rf /"}, sb_term,
           build_runtime_policy(True), build_runtime_permissions(["terminal"])),
        ea("ea_native_focus", {"type": "native_focus", "window": "app"}, sb_native, pol,
           build_runtime_permissions(["native"])),
        ea("ea_sandbox_forbidden", {"type": "vm_execute", "payload": {"cmd": "x"}}, sb, pol, perms_browser),
        ea("ea_permission_denied", {"type": "browser_click", "selector": "#x"}, sb, pol, perms_none),
        ea("ea_no_permissions", {"type": "browser_click", "selector": "#x"}, sb, pol, None),
        ea("ea_unicode", {"type": "browser_click", "selector": ".café-\U0001F600"}, sb, pol, perms_browser),
    ]

    # replay_runtime_execution
    def rp(name, actions, transactions=None, mutations=None, tick=0):
        return e(name, {"actions": actions, "transactions": transactions, "mutations": mutations, "tick": tick},
                 replay_runtime_execution(actions, transactions=transactions, mutations=mutations, tick=tick))

    out["replay_runtime_execution"] = [
        rp("rp_empty", []),
        rp("rp_actions_order", [{"id": "z"}, {"id": "a"}, {"id": "m"}]),
        rp("rp_mutations_tick", mutations=[{"tick": 2, "ordered_index": 0}, {"tick": 1, "ordered_index": 1},
                                           {"tick": 1, "ordered_index": 0}], actions=[]),
        rp("rp_full", [{"id": "a2"}, {"id": "a1"}],
           transactions=[{"transaction_id": "t2"}, {"transaction_id": "t1"}],
           mutations=[{"tick": 0, "ordered_index": 1}, {"tick": 0, "ordered_index": 0}], tick=5),
    ]

    # simulate_runtime_execution
    def sim(name, actions, sandbox=None, tick=0):
        return e(name, {"actions": actions, "sandbox": sandbox, "tick": tick},
                 simulate_runtime_execution(actions, sandbox=sandbox, tick=tick))

    out["simulate_runtime_execution"] = [
        sim("sim_empty", []),
        sim("sim_clicks", [{"type": "browser_click", "selector": "#a"},
                           {"type": "browser_click", "selector": "#b"}]),
        sim("sim_mixed", [{"type": "browser_click", "selector": "#a"},
                          {"type": "browser_click", "selector": ""},
                          {"type": "vm_execute"}]),
        sim("sim_native", [{"type": "native_focus", "window": "w"}], sandbox=build_runtime_sandbox("native")),
    ]

    # run_execution_runtime
    def rer(name, **kw):
        return e(name, kw, run_execution_runtime(**kw))

    out["run_execution_runtime"] = [
        rer("run_default"),
        rer("run_browser_actions", sources={"actions": [{"type": "browser_click", "selector": "#go"}]}),
        rer("run_terminal", runtime="terminal", sources={"actions": [{"type": "terminal_command", "command": "pwd"}]}),
        rer("run_native", runtime="native"),
        rer("run_simulate", simulate=True, sources={"actions": [{"type": "browser_click", "selector": "#s"}]}),
        rer("run_checkpoint", stored={"checkpoint": {"state": {"browser": {"url": "x"}}}}),
        rer("run_workers", workers=[{"worker_id": "w2"}, {"worker_id": "w1"}],
            sources={"actions": [{"type": "browser_click", "selector": "#m"}]}),
        rer("run_tick", tick=7, sources={"actions": [{"type": "browser_click", "selector": "#t"}]}),
    ]

    # run_execution_for_extraction (empty memory_path/key -> no FS)
    def rfe(name, **kw):
        return e(name, kw, run_execution_for_extraction(**kw))

    out["run_execution_for_extraction"] = [
        rfe("rfe_disabled", execution_runtime=False),
        rfe("rfe_default"),
        rfe("rfe_no_merge", merge_graph=False),
        rfe("rfe_simulate", simulate_execution=True),
        rfe("rfe_actions", sources={"actions": [{"type": "browser_click", "selector": "#go"}]}),
    ]

    # ---- engine-level parity (covers internal branches; Python is the oracle) -----------
    from core.execution.runtime_transition_engine import apply_runtime_transition
    from core.execution.runtime_mutation_engine import track_runtime_mutations
    from core.execution.runtime_queue_engine import enqueue_runtime_action, dequeue_runtime_action
    from core.execution.runtime_scheduler_engine import schedule_runtime_execution
    from core.execution.runtime_policy_engine import enforce_runtime_policy
    from core.execution.runtime_permissions_engine import validate_runtime_permissions
    from core.execution.runtime_transaction_engine import (
        begin_runtime_transaction, commit_runtime_transaction)
    from core.execution.runtime_worker_engine import build_runtime_workers
    from core.execution.runtime_federation_engine import federate_runtime_execution
    from core.execution.runtime_coordination_engine import coordinate_runtime_execution
    from core.execution.runtime_recovery_engine import recover_runtime_execution
    from core.execution.runtime_action_engine import build_runtime_action
    from core.runtime_graph.runtime_graph_engine import build_runtime_graph as build_unified_graph

    out["apply_runtime_transition"] = [
        e(f"t_{s}_{ev}", {"state": s, "event": ev}, apply_runtime_transition(s, ev))
        for s, ev in [("idle", "enqueue"), ("idle", "simulate"), ("queued", "execute"),
                      ("queued", "rollback"), ("executing", "commit"), ("executing", "fail"),
                      ("failed", "recover"), ("committed", "noop"), ("unknown", "enqueue"),
                      ("recovering", "x"), ("simulating", "execute")]
    ]
    out["build_runtime_policy"] = [
        e("pol_default", {"allow_terminal": False}, build_runtime_policy()),
        e("pol_terminal", {"allow_terminal": True}, build_runtime_policy(allow_terminal=True)),
    ]
    out["enforce_runtime_policy"] = [
        e("enf_ok", {"policy": pol, "action": {"action_type": "browser_click"}, "mutation_count": 0,
                     "action_count": 0}, enforce_runtime_policy(pol, {"action_type": "browser_click"}, 0, 0)),
        e("enf_forbidden", {"policy": pol, "action": {"action_type": "terminal_command"}, "mutation_count": 0,
                            "action_count": 0}, enforce_runtime_policy(pol, {"action_type": "terminal_command"}, 0, 0)),
        e("enf_over_mut", {"policy": pol, "action": {"action_type": "browser_click"}, "mutation_count": 500,
                           "action_count": 0}, enforce_runtime_policy(pol, {"action_type": "browser_click"}, 500, 0)),
        e("enf_no_browser_mut", {"policy": build_runtime_policy(), "action": {"action_type": "browser_click"},
                                 "mutation_count": 0, "action_count": 2000},
          enforce_runtime_policy(build_runtime_policy(), {"action_type": "browser_click"}, 0, 2000)),
    ]
    out["validate_runtime_permissions"] = [
        e(f"vp_{at}", {"permissions": perms_browser, "runtime": "browser", "action_type": at},
          validate_runtime_permissions(perms_browser, "browser", at))
        for at in ["browser_click", "terminal_command", "native_focus", "vm_execute", "connector_x", "other"]
    ]
    out["track_runtime_mutations"] = [
        e(f"tm_{k}", {"prior": [], "mutation": {"kind": k, "target": "x", "tick": 1}},
          track_runtime_mutations(prior=[], mutation={"kind": k, "target": "x", "tick": 1}))
        for k in ["dom", "native", "workflow", "sync", "memory", "other"]
    ] + [e("tm_none", {"prior": [{"kind": "dom", "tick": 0, "ordered_index": 0}], "mutation": None},
           track_runtime_mutations(prior=[{"kind": "dom", "tick": 0, "ordered_index": 0}], mutation=None))]
    act = build_runtime_action("browser_click", "browser", {"selector": "#a"}, tick=0)
    out["enqueue_runtime_action"] = [
        e("enq_empty", {"queue": [], "action": act, "priority": 0}, enqueue_runtime_action([], act, priority=0)),
        e("enq_priority", {"queue": [{"action": act, "priority": 0, "order": 0}], "action": act, "priority": 5},
          enqueue_runtime_action([{"action": act, "priority": 0, "order": 0}], act, priority=5)),
    ]
    out["dequeue_runtime_action"] = [
        e("deq_empty", {"queue": []}, dequeue_runtime_action([])),
        e("deq_one", {"queue": [{"action": act, "priority": 0, "order": 0}]},
          dequeue_runtime_action([{"action": act, "priority": 0, "order": 0}])),
    ]
    out["schedule_runtime_execution"] = [
        e("sch_empty", {"actions": [], "tick": 0}, schedule_runtime_execution([], tick=0)),
        e("sch_actions", {"actions": [{"id": "z"}, {"id": "a"}], "tick": 3},
          schedule_runtime_execution([{"id": "z"}, {"id": "a"}], tick=3)),
    ]
    out["begin_runtime_transaction"] = [
        e("tx_begin", {"tick": 0, "checkpoint_id": ""}, begin_runtime_transaction(0, "")),
        e("tx_begin_cp", {"tick": 4, "checkpoint_id": "cp1"}, begin_runtime_transaction(4, "cp1")),
    ]
    _tx = begin_runtime_transaction(0, "")
    out["commit_runtime_transaction"] = [
        e("tx_commit", {"transaction": _tx}, commit_runtime_transaction(_tx)),
    ]
    out["build_runtime_workers"] = [
        e("wk_empty", {"nodes": []}, build_runtime_workers([])),
        e("wk_nodes", {"nodes": [{"worker_id": "w2"}, {"node_id": "w1", "runtime": "native", "synced": False}]},
          build_runtime_workers([{"worker_id": "w2"}, {"node_id": "w1", "runtime": "native", "synced": False}])),
    ]
    fed = federate_runtime_execution([{"worker_id": "w1"}, {"worker_id": "w2"}], [{"id": "a1"}])
    out["federate_runtime_execution"] = [
        e("fed_empty", {"workers": [], "actions": None}, federate_runtime_execution([], None)),
        e("fed_actions", {"workers": [{"worker_id": "w1"}, {"worker_id": "w2"}], "actions": [{"id": "a1"}]}, fed),
    ]
    out["coordinate_runtime_execution"] = [
        e("coord_full", {"queue": [{"priority": 1, "order": 0}], "federation": fed,
                         "workflow": {"id": "wf"}, "sync_state": {"s": 1}},
          coordinate_runtime_execution([{"priority": 1, "order": 0}], fed, workflow={"id": "wf"}, sync_state={"s": 1})),
        e("coord_empty", {"queue": [], "federation": fed, "workflow": None, "sync_state": None},
          coordinate_runtime_execution([], fed, workflow=None, sync_state=None)),
    ]
    out["recover_runtime_execution"] = [
        e("rec_empty", {"failed_actions": None, "checkpoint": None, "interrupted_workflows": None},
          recover_runtime_execution()),
        e("rec_failed", {"failed_actions": [{"id": "z"}, {"id": "a"}], "checkpoint": {"state": 1},
                         "interrupted_workflows": [{"w": 1}]},
          recover_runtime_execution(failed_actions=[{"id": "z"}, {"id": "a"}], checkpoint={"state": 1},
                                    interrupted_workflows=[{"w": 1}])),
    ]
    out["build_runtime_action"] = [
        e("ba_browser", {"action_type": "browser_click", "runtime": "browser", "payload": {"selector": "#x"},
                         "tick": 2}, build_runtime_action("browser_click", "browser", {"selector": "#x"}, tick=2)),
        e("ba_empty", {"action_type": "noop", "runtime": "browser", "payload": None, "tick": 0},
          build_runtime_action("noop", "browser", None, tick=0)),
    ]
    out["build_unified_runtime_graph"] = [
        e("ug_empty", {"runtime_irs": []}, build_unified_graph([])),
        e("ug_merge", {"runtime_irs": [
            {"ir": "a", "nodes": [{"id": "n2"}, {"id": "n1"}], "edges": [{"from": "n1", "to": "n2", "relation": "r"}]},
            {"ir": "b", "nodes": [{"id": "n1"}, {"id": ""}], "edges": [{"from": "n2", "to": "n1"}]}]},
          build_unified_graph([
            {"ir": "a", "nodes": [{"id": "n2"}, {"id": "n1"}], "edges": [{"from": "n1", "to": "n2", "relation": "r"}]},
            {"ir": "b", "nodes": [{"id": "n1"}, {"id": ""}], "edges": [{"from": "n2", "to": "n1"}]}])),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s9.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors {counts}\n")


if __name__ == "__main__":
    main()
