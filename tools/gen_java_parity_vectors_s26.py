#!/usr/bin/env python3
"""Session-26 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s26.py <out.json>

Covers run_application_cognition (portable html="" contract) + its pure sub-engines. Python is
the oracle; every vector uses html="" so the output is bs4-independent.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.application.application_cognition_orchestrator import run_application_cognition
from core.application.application_state_engine import build_application_state
from core.application.application_transition_engine import build_application_transitions
from core.application.action_graph_engine import build_action_graph
from core.application.workflow_graph_engine import build_workflow_graph
from core.application.application_intent_engine import resolve_application_intent
from core.application.application_context_engine import build_application_context
from core.application.navigation_semantic_engine import build_navigation_semantics
from core.application.application_recovery_engine import recover_application_runtime
from core.application.ui_semantic_engine import extract_ui_semantics
from core.application.form_runtime_engine import build_form_runtime
from core.application.dashboard_runtime_engine import build_dashboard_runtime


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 26: application cognition, html='' contract)"}

    runs = [
        ("default", dict(url="https://app", html="")),
        ("full", dict(url="https://app/dash", html="", interactions=[{"action": "click", "selector": "#a"},
                      {"action": "modal_open"}, {"action": "fill"}], objective="extract_dashboard",
                      authenticated=True, identity={"profile_id": "p1"}, adaptive_runtime={"x": 1},
                      route_history=[{"path": "/a"}, {"path": "/b"}], modals=[{"id": "m1"}])),
        ("login", dict(url="https://x/login", html="", objective="login", interactions=[{"action": "fill"}])),
        ("memory", dict(url="https://x", html="", objective="monitor_metrics",
                        memory={"application_state": {"route": "https://prev", "authenticated": True}})),
        ("mem_fields", dict(url="https://x", html="", objective="login",
                        memory={"workflows": {"old": 1}, "forms": {"f": 9},
                                "application_state": {"route": "/p"}})),
    ]
    out["run_application_cognition"] = [ev(n, {**kw}, run_application_cognition(**kw)) for n, kw in runs]

    # ---- engine-level parity ----
    out["extract_ui_semantics"] = [ev("ui_empty", {"html": ""}, extract_ui_semantics(""))]
    out["build_form_runtime"] = [ev("form_empty", {"html": ""}, build_form_runtime(""))]
    out["build_dashboard_runtime"] = [ev("dash_empty", {"html": ""}, build_dashboard_runtime(""))]
    out["build_navigation_semantics"] = [
        ev("nav_route", {"route": "https://app", "route_history": None},
           build_navigation_semantics("", "https://app", None)),
        ev("nav_history", {"route": "https://app", "route_history": [{"path": "/a"}, {"path": "/b"}]},
           build_navigation_semantics("", "https://app", [{"path": "/a"}, {"path": "/b"}])),
    ]
    ST = build_application_state(route="https://app", forms=[], modals=[{"id": "m"}], widgets=[], tabs=[],
                                authenticated=True)
    out["recover_application_runtime"] = [
        ev("recover", {"state": ST}, recover_application_runtime("", ST)),
        ev("recover_empty", {"state": {"route": "/", "modals": [], "authenticated": False}},
           recover_application_runtime("", {"route": "/", "modals": [], "authenticated": False})),
    ]
    out["build_application_state"] = [
        ev("state", {"route": "https://app", "forms": [{"f": 1}], "modals": [{"m": 1}], "widgets": [{"w": 1}],
                     "tabs": [{"t": 1}], "authenticated": True},
           build_application_state(route="https://app", forms=[{"f": 1}], modals=[{"m": 1}], widgets=[{"w": 1}],
                                   tabs=[{"t": 1}], authenticated=True)),
        ev("minimal", {"route": "r"}, build_application_state(route="r")),
        ev("long_route", {"route": "a" * 2100, "forms": [], "modals": [], "widgets": [], "tabs": [],
                          "authenticated": False},
           build_application_state(route="a" * 2100, forms=[], modals=[], widgets=[], tabs=[], authenticated=False)),
    ]
    STATES = [{"route": "/a"}, {"route": "/b"}, {"route": "/c"}]
    out["build_application_transitions"] = [
        ev("trans", {"states": STATES}, {"transitions": build_application_transitions(STATES)}),
        ev("trans_one", {"states": [{"route": "/a"}]}, {"transitions": build_application_transitions([{"route": "/a"}])}),
    ]
    IX = [{"action": "click", "selector": "#a"}, {"action": "fill"}, {"action": "modal_open"}]
    out["build_action_graph"] = [
        ev("actions", {"interactions": IX}, build_action_graph(IX)),
        ev("actions_empty", {"interactions": []}, build_action_graph([])),
    ]
    TR = build_application_transitions(STATES)
    out["build_workflow_graph"] = [
        ev("wf", {"states": STATES, "transitions": TR, "actions": IX}, build_workflow_graph(STATES, TR, IX)),
        ev("wf_empty", {"states": [], "transitions": [], "actions": []}, build_workflow_graph([], [], [])),
    ]
    out["resolve_application_intent"] = [
        ev("intent_known", {"objective": "extract_dashboard"}, resolve_application_intent("extract_dashboard")),
        ev("intent_unknown", {"objective": "custom"}, resolve_application_intent("custom")),
    ]
    out["build_application_context"] = [
        ev("context", {"url": "https://app", "state": {"route": "/r", "authenticated": True},
                       "identity": {"profile_id": "p1"}},
           build_application_context("https://app", {"route": "/r", "authenticated": True}, {"profile_id": "p1"})),
        ev("context_default", {"url": "https://app", "state": {}, "identity": {}},
           build_application_context("https://app", {}, {})),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s26.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
