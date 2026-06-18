#!/usr/bin/env python3
"""Session-6 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s6.py <out.json>

Covers the single in-scope API build_interaction_graph
(core.interaction.interaction_graph_engine) — proven dependency-clean
(JAVA_SESSION_6_ANALYSIS.md). Each entry stores the inputs plus the canonical
`stable_serialize` of the Python output and its `compute_kaalka_hash`; the Java
test reconstructs the inputs, recomputes, and asserts byte-equality.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.interaction.interaction_graph_engine import build_interaction_graph


def graph(name, interactions):
    return {
        "name": name,
        "inputs": {"interactions": interactions},
        "serialized": stable_serialize(build_interaction_graph(interactions)),
        "hash": compute_kaalka_hash(build_interaction_graph(interactions)),
    }


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 6: build_interaction_graph)"}

    vectors = [
        # empty graph
        graph("ig_empty", []),
        # single interaction (each relation/type branch)
        graph("ig_single_click", [{"id": "n1", "action": "click", "selector": "#submit"}]),
        graph("ig_single_fill_form", [{"action": "fill", "selector": "input#name"}]),
        graph("ig_select_submission", [{"action": "select", "selector": "select#country"}]),
        graph("ig_wait_navigation", [{"action": "wait", "selector": ""}]),
        graph("ig_hover_passthrough", [{"action": "hover", "selector": ".menu"}]),
        graph("ig_empty_action_transition", [{"selector": ".x"}]),
        # node-type detection (modal / tab; tab wins over modal)
        graph("ig_modal", [{"action": "click", "selector": ".Modal-Dialog"}]),
        graph("ig_tab", [{"action": "click", "selector": "#TabPanel"}]),
        graph("ig_modal_and_tab", [{"action": "click", "selector": "modal-tab"}]),
        # multiple interactions + ordering (edges chain in sequence)
        graph("ig_multiple_chain", [
            {"id": "a", "action": "click", "selector": "#a"},
            {"id": "b", "action": "fill", "selector": "input#b"},
            {"id": "c", "action": "select", "selector": "select#c"},
            {"id": "d", "action": "wait", "selector": ""},
        ]),
        # ordering: same set, different order -> different graph
        graph("ig_order_ab", [
            {"id": "x", "action": "click", "selector": "#x"},
            {"id": "y", "action": "fill", "selector": "#y"},
        ]),
        graph("ig_order_ba", [
            {"id": "y", "action": "fill", "selector": "#y"},
            {"id": "x", "action": "click", "selector": "#x"},
        ]),
        # malformed interactions (missing keys -> defaults; extra keys ignored)
        graph("ig_malformed_missing", [
            {},
            {"action": "click"},
            {"selector": "#z", "extra": "ignored"},
        ]),
        # non-string id (int) and None id -> str() coercion
        graph("ig_id_int", [{"id": 5, "action": "click", "selector": "#a"}]),
        graph("ig_id_none", [{"id": None, "action": "click", "selector": "#a"}]),
        # cyclic / repeated node ids (edges all chain through the reused id)
        graph("ig_repeated_ids", [
            {"id": "loop", "action": "click", "selector": "#a"},
            {"id": "loop", "action": "fill", "selector": "#b"},
            {"id": "loop", "action": "click", "selector": "#a"},
        ]),
        # unicode (CJK id, emoji + accented selector)
        graph("ig_unicode", [{"id": "按钮", "action": "click",
                              "selector": ".café-\U0001F600"}]),
        # normalization (NFKC ligature + trailing whitespace stripped by stable_serialize)
        graph("ig_normalization", [{"id": "ñ", "action": "click",
                                    "selector": "ﬁle  "}]),
        # replay case (realistic interaction log)
        graph("ig_replay_log", [
            {"id": "nav", "action": "wait", "selector": "body"},
            {"id": "email", "action": "fill", "selector": "input#email"},
            {"id": "pass", "action": "fill", "selector": "input#password"},
            {"id": "remember", "action": "click", "selector": "input.remember-tab"},
            {"id": "submit", "action": "click", "selector": "button#login"},
        ]),
    ]

    out["build_interaction_graph"] = vectors

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s6.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    sys.stderr.write(f"wrote {target}: {len(vectors)} vectors\n")


if __name__ == "__main__":
    main()
