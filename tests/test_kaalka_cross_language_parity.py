"""Cross-language parity tests against javascript_vectors.json reference."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.crypto.kaalka_runtime_engine import (
    compute_deterministic_hash,
    decrypt_value,
    derive_kaalka_time_key,
    encrypt_value,
)
from core.determinism.normalization import normalize_runtime_value, stable_serialize
from core.determinism.runtime_graph_parity import build_parity_runtime_graph

ROOT = Path(__file__).resolve().parents[1]
JS_VECTORS = ROOT / "validation" / "parity" / "javascript_vectors.json"

CASE_VALUES: dict[str, tuple[object, str]] = {
    "probe-1": ("probe", "k"),
    "probe-2": ("runtime", "kaalka-key"),
    "unicode": ("café\r\n日本語 🚀", "uni"),
    "emoji": ("runtime 🚀", "emoji-key"),
    "crlf": ("line\r\nbreak", "crlf-key"),
    "session": ('{"cookies":[],"headers":{}}', "session-key"),
    "nested-object": (
        {"z": 3, "a": {"b": 2, "timestamp": 999}, "m": [1, {"uuid": "x"}]},
        "nested",
    ),
    "array": ([{"id": "b"}, {"id": "a"}], "arr"),
    "dom": (
        '<div data-reactroot="" nonce="abc">Hi <span data-v-1="x">🚀</span></div>',
        "dom-key",
    ),
    "memory-graph": (
        {"memories": [{"id": "m2"}, {"id": "m1"}], "merged": True},
        "mem",
    ),
}


def test_normalize_crlf():
    assert normalize_runtime_value("a\r\n") == "a"


def test_encrypt_roundtrip():
    enc = encrypt_value("probe", "k")
    assert decrypt_value(enc["encrypted"], "k")["decrypted"] == "probe"


@pytest.mark.skipif(not JS_VECTORS.exists(), reason="javascript_vectors.json required")
@pytest.mark.parametrize("vector_id", list(CASE_VALUES.keys()) + ["graph"])
def test_matches_javascript_vector(vector_id: str):
    doc = json.loads(JS_VECTORS.read_text(encoding="utf-8"))
    jv = next(v for v in doc["vectors"] if v["id"] == vector_id)
    if vector_id == "graph":
        value = build_parity_runtime_graph(
            {"nodes": [{"id": "b"}, {"id": "a"}], "edges": []}
        )
        key = "graph-key"
    else:
        value, key = CASE_VALUES[vector_id]
    assert stable_serialize(value) == jv["serialized"]
    assert derive_kaalka_time_key(key) == jv["time_key"]
    assert compute_deterministic_hash(value) == jv["hash"]
    assert encrypt_value(value, key)["encrypted"] == jv["encrypted"]
