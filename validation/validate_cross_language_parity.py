#!/usr/bin/env python3
"""
Cross-language parity validator: Python vectors vs javascript_vectors.json reference.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from core.crypto.kaalka_runtime_engine import (
    compute_deterministic_hash,
    decrypt_value,
    derive_kaalka_time_key,
    encrypt_value,
)
from core.determinism.normalization import stable_serialize
from core.determinism.runtime_graph_parity import build_parity_runtime_graph

ROOT = Path(__file__).resolve().parents[1]
PARITY_DIR = ROOT / "validation" / "parity"
JS_VECTORS = PARITY_DIR / "javascript_vectors.json"
PY_VECTORS = PARITY_DIR / "python_vectors.json"
REPORT = ROOT / "docs" / "archive" / "FINAL_CROSS_LANGUAGE_PARITY_REPORT.md"

CASES: list[dict[str, Any]] = [
    {"id": "probe-1", "plaintext": "probe", "key": "k"},
    {"id": "probe-2", "plaintext": "runtime", "key": "kaalka-key"},
    {"id": "unicode", "plaintext": "café\r\n日本語 🚀", "key": "uni"},
    {"id": "emoji", "plaintext": "runtime 🚀", "key": "emoji-key"},
    {"id": "crlf", "plaintext": "line\r\nbreak", "key": "crlf-key"},
    {"id": "session", "plaintext": '{"cookies":[],"headers":{}}', "key": "session-key"},
    {
        "id": "nested-object",
        "payload": {"z": 3, "a": {"b": 2, "timestamp": 999}, "m": [1, {"uuid": "x"}]},
        "key": "nested",
    },
    {
        "id": "graph",
        "payload": build_parity_runtime_graph(
            {"nodes": [{"id": "b"}, {"id": "a"}], "edges": []}
        ),
        "key": "graph-key",
    },
    {"id": "array", "payload": [{"id": "b"}, {"id": "a"}], "key": "arr"},
    {
        "id": "dom",
        "dom_html": '<div data-reactroot="" nonce="abc">Hi <span data-v-1="x">🚀</span></div>',
        "key": "dom-key",
    },
    {
        "id": "memory-graph",
        "payload": {"memories": [{"id": "m2"}, {"id": "m1"}], "merged": True},
        "key": "mem",
    },
]


def _value(case: dict[str, Any]) -> Any:
    if "plaintext" in case:
        return case["plaintext"]
    if "dom_html" in case:
        return case["dom_html"]
    return case["payload"]


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    value = _value(case)
    key = case["key"]
    serialized = stable_serialize(value)
    time_key = derive_kaalka_time_key(key)
    enc = encrypt_value(value, key)["encrypted"]
    dec = decrypt_value(enc, key)["decrypted"]
    enc2 = encrypt_value(value, key)["encrypted"]
    return {
        "id": case["id"],
        "serialized": serialized,
        "time_key": time_key,
        "hash": compute_deterministic_hash(value),
        "encrypted": enc,
        "decrypt_ok": dec == serialized,
        "deterministic": enc == enc2,
    }


def main() -> int:
    PARITY_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "docs" / "archive").mkdir(parents=True, exist_ok=True)

    py_vectors = [run_case(c) for c in CASES]
    py_doc = {
        "algorithm": "webweavex-formula+kaalka@5.0.0",
        "kaalka": "5.0.0",
        "vectors": py_vectors,
    }
    PY_VECTORS.write_text(json.dumps(py_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if not JS_VECTORS.exists():
        print(f"Missing reference: {JS_VECTORS}", file=sys.stderr)
        return 1

    js_doc = json.loads(JS_VECTORS.read_text(encoding="utf-8-sig"))
    js_by_id = {v["id"]: v for v in js_doc.get("vectors", [])}

    results: list[dict[str, Any]] = []
    all_pass = True
    for pv in py_vectors:
        jv = js_by_id.get(pv["id"])
        if not jv:
            results.append({"id": pv["id"], "status": "missing_js_vector"})
            all_pass = False
            continue
        checks = {
            "serialized": pv["serialized"] == jv.get("serialized"),
            "time_key": pv["time_key"] == jv.get("time_key"),
            "hash": pv["hash"] == jv.get("hash"),
            "encrypted": pv["encrypted"] == jv.get("encrypted"),
            "decrypt_ok": pv["decrypt_ok"],
            "deterministic": pv["deterministic"],
        }
        ok = all(checks.values())
        if not ok:
            all_pass = False
        results.append({"id": pv["id"], "pass": ok, **checks})

    lines = [
        "# FINAL CROSS-LANGUAGE PARITY REPORT",
        "",
        f"**Status:** {'VERIFIED' if all_pass else 'FAILED'}",
        "",
        "## Summary",
        "",
        "| Gate | Result |",
        "|------|--------|",
        f"| Normalization / serialization | {'PASS' if all(r.get('serialized') for r in results if 'serialized' in r) else 'FAIL'} |",
        f"| Time-key derivation | {'PASS' if all(r.get('time_key') for r in results if 'time_key' in r) else 'FAIL'} |",
        f"| Hash parity | {'PASS' if all(r.get('hash') for r in results if 'hash' in r) else 'FAIL'} |",
        f"| Ciphertext parity | {'PASS' if all(r.get('encrypted') for r in results if 'encrypted' in r) else 'FAIL'} |",
        f"| Python self-consistency | {'PASS' if all(pv['decrypt_ok'] and pv['deterministic'] for pv in py_vectors) else 'FAIL'} |",
        "",
        "## Per-vector results",
        "",
        "```json",
        json.dumps(results, indent=2),
        "```",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PARITY_DIR.joinpath("parity_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
