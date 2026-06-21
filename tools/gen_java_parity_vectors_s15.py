#!/usr/bin/env python3
"""Session-15 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s15.py <out.json>

Covers the dependency-clean standalone API recover_modal_runtime (page=None path).
Python is the oracle.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.adaptive.modal_recovery_engine import recover_modal_runtime


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 15: modal recovery)"}

    htmls = [
        ("none", ""),
        ("cookie", "<div id='cookie-accept'>Accept</div>"),
        ("aria_close", "<button aria-label='Close'>x</button>"),
        ("button_accept", "<button class='accept'>OK</button>"),
        ("modal_close", "<span class='modal-close'></span>"),
        ("first_wins", "<div class='modal-close'></div><div id='cookie-accept'></div>"),
        ("no_match", "<p>nothing here</p>"),
        ("case_insensitive", "<DIV ID='COOKIE-ACCEPT'></DIV>"),
        ("unicode", "<div id='cookie-accept'>café \U0001F600</div>"),
    ]
    out["recover_modal_runtime"] = [
        ev("modal_" + name, {"html": html}, recover_modal_runtime(None, html))
        for name, html in htmls
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s15.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
