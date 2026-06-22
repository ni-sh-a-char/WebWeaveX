#!/usr/bin/env python3
"""Session-21 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s21.py <out.json>

Covers heal_selector for the portable empty-HTML contract (html="" -> semantic anchor yields
nothing, output is a pure function of selector + dom_nodes). Python is the oracle.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize
from core.adaptive.selector_healing_engine import heal_selector


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 21: heal_selector empty-HTML contract)"}

    cases = [
        ("text_match", "#submit-button", [{"tag": "button", "text": "Submit Button now"},
                                          {"tag": "div", "text": "other"}]),
        ("text_then_attr", ".save-btn", [{"tag": "a", "text": "save btn here",
                                          "attrs": {"id": "x", "data-testid": "t"}}]),
        ("attr_only", "#missing", [{"tag": "span", "attrs": {"name": "field1", "aria-label": "Field"}}]),
        ("attr_sorted", "#none", [{"tag": "div", "attrs": {"name": "n", "id": "i", "aria-label": "a"}}]),
        ("structural_fallback", "#nothing", [{"tag": "section"}]),
        ("empty_nodes", ".x", []),
        ("unicode", "#café-button", [{"tag": "button", "text": "Café Button click"}]),
        ("class_token", ".user_name", [{"tag": "label", "text": "the user name field"}]),
        ("plain_selector", "loginform", [{"tag": "form", "text": "loginform area"}]),
        ("attr_non_dict", "#a", [{"tag": "div", "attrs": "notadict"}, {"tag": "p", "attrs": {"id": "y"}}]),
        ("first_no_match", "#submit", [{"tag": "div", "text": "nope"},
                                       {"tag": "button", "text": "submit here now"}]),
        ("long_text", "#go", [{"tag": "button", "text": "go " + "x" * 150}]),
        ("long_attr", "#none", [{"tag": "div", "attrs": {"id": "i" + "d" * 250}}]),
        ("empty_token", "", [{"tag": "div", "text": "anything"}]),
        ("attr_skip_key", "#zz", [{"tag": "div", "attrs": {"class": "c", "role": "r", "id": "real"}}]),
        ("no_match_fallback", "#zzz", [{"tag": "section", "text": "unrelated"},
                                       {"tag": "p", "text": "more"}]),
        ("over_cap", "#target", [{"tag": "div", "text": "n%d" % i} for i in range(101)]
            + [{"tag": "button", "text": "target found"}]),
        ("attr_no_match_key", "#x", [{"tag": "div", "attrs": {"class": "c", "role": "r", "style": "s"}}]),
        ("attr_empty_dict", "#y", [{"tag": "span", "attrs": {}}, {"tag": "p", "attrs": {"name": "ok"}}]),
    ]
    out["heal_selector"] = [
        ev(name, {"selector": sel, "dom_nodes": nodes}, heal_selector(sel, nodes, ""))
        for name, sel, nodes in cases
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s21.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
