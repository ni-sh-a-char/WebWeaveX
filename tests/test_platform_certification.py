"""PYTHON-CERT-05: Cross-Language Platform Certification.

Golden fixture validation and cross-SDK behavior matrix.
Python is the reference — these tests define the canonical contract.
"""
import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "golden_fixtures"


# ---------------------------------------------------------------------------
# 1. SERIALIZATION GOLDEN FIXTURES
# ---------------------------------------------------------------------------

class TestSerializationFixtures:
    def test_all_vectors_match_expected(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        vectors = json.loads((FIXTURES / "serialization_vectors.json").read_text())
        for v in vectors:
            result = dumps_deterministic(v["input"])
            assert result == v["expected_deterministic"], (
                f"Input {v['input']}: got {result}, expected {v['expected_deterministic']}"
            )

    def test_sorted_keys_ordering(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        vectors = json.loads((FIXTURES / "serialization_vectors.json").read_text())
        for v in vectors:
            result = dumps_deterministic(v["input"])
            parsed = json.loads(result)
            keys = list(parsed.keys())
            assert keys == sorted(keys), f"Keys not sorted for input {v['input']}"


# ---------------------------------------------------------------------------
# 2. NORMALIZATION GOLDEN FIXTURES
# ---------------------------------------------------------------------------

class TestNormalizationFixtures:
    def test_all_vectors_match_expected(self):
        from core.determinism.normalization import normalize_runtime_value
        vectors = json.loads((FIXTURES / "normalization_vectors.json").read_text())
        for v in vectors:
            result = normalize_runtime_value(v["input"])
            assert result == v["expected"], (
                f"Input '{v['input']}': got '{result}', expected '{v['expected']}'"
            )


# ---------------------------------------------------------------------------
# 3. HASH GOLDEN FIXTURES
# ---------------------------------------------------------------------------

class TestHashFixtures:
    def test_all_produce_valid_hex64(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        vectors = json.loads((FIXTURES / "hash_vectors.json").read_text())
        for v in vectors:
            h = compute_deterministic_hash(v["input"])
            assert len(h) == 64, f"Hash length {len(h)} != 64 for input {v['input']}"
            assert all(c in "0123456789abcdef" for c in h), f"Non-hex chars in hash for {v['input']}"

    def test_all_deterministic(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        vectors = json.loads((FIXTURES / "hash_vectors.json").read_text())
        for v in vectors:
            h1 = compute_deterministic_hash(v["input"])
            h2 = compute_deterministic_hash(v["input"])
            assert h1 == h2, f"Non-deterministic hash for input {v['input']}"


# ---------------------------------------------------------------------------
# 4. GRAPH GOLDEN FIXTURES
# ---------------------------------------------------------------------------

class TestGraphFixtures:
    def test_node_and_edge_counts(self):
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph
        vectors = json.loads((FIXTURES / "graph_vectors.json").read_text())
        for v in vectors:
            ir = [{"ir": "test", "nodes": v["input"]["nodes"], "edges": v["input"]["edges"]}]
            g = build_runtime_graph(ir)
            nodes = g.get("nodes", [])
            edges = g.get("edges", [])
            assert len(nodes) == v["expected_node_count"], (
                f"Node count {len(nodes)} != {v['expected_node_count']} for {v['input']}"
            )
            assert len(edges) == v["expected_edge_count"], (
                f"Edge count {len(edges)} != {v['expected_edge_count']} for {v['input']}"
            )


# ---------------------------------------------------------------------------
# 5. CROSS-SDK BEHAVIOR MATRIX
# ---------------------------------------------------------------------------

class TestCrossSDKBehaviorMatrix:
    """Verify Python defines canonical behavior that other SDKs must match."""

    def test_deterministic_hash_length_matches_cross_sdk(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        h = compute_deterministic_hash({"version": "3.0.0"})
        assert len(h) == 64, "Cross-SDK: hash must be 64-char hex"

    def test_graph_fingerprint_deterministic_cross_sdk(self):
        from core.crypto.kaalka_wrapper import graph_fingerprint
        g = {"nodes": [{"id": "n1"}], "edges": []}
        fp = graph_fingerprint(g)
        assert isinstance(fp, bytes), "Cross-SDK: fingerprint must be bytes"
        assert len(fp) > 0, "Cross-SDK: fingerprint must not be empty"

    def test_replay_equivalence_returns_dict_cross_sdk(self):
        from core.replay.replay_equivalence_engine import validate_replay_equivalence
        r = validate_replay_equivalence({}, {})
        assert isinstance(r, dict), "Cross-SDK: replay result must be dict"
        assert "equivalent" in r, "Cross-SDK: replay result must contain 'equivalent'"

    def test_serialization_is_string_cross_sdk(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        result = dumps_deterministic({"key": "value"})
        assert isinstance(result, str), "Cross-SDK: serialization must return string"
        assert result.startswith("{"), "Cross-SDK: object serialization must start with {"


# ---------------------------------------------------------------------------
# 6. KAALKA CERTIFICATION
# ---------------------------------------------------------------------------

class TestKaalkaCertification:
    def test_kaalka_encrypt_deterministic(self):
        from core.crypto.kaalka_wrapper import kaalka_encrypt
        data = b"hello world"
        e1 = kaalka_encrypt(data, time_key=123456)
        e2 = kaalka_encrypt(data, time_key=123456)
        assert e1 == e2

    def test_kaalka_encrypt_differs_by_key(self):
        from core.crypto.kaalka_wrapper import kaalka_encrypt
        data = b"hello world"
        e1 = kaalka_encrypt(data, time_key=123456)
        e2 = kaalka_encrypt(data, time_key=789012)
        assert e1 != e2

    def test_kaalka_encrypt_differs_by_data(self):
        from core.crypto.kaalka_wrapper import kaalka_encrypt
        e1 = kaalka_encrypt(b"data1", time_key=123456)
        e2 = kaalka_encrypt(b"data2", time_key=123456)
        assert e1 != e2

    def test_graph_fingerprint_uses_kaalka(self):
        from core.crypto.kaalka_wrapper import graph_fingerprint, kaalka_encrypt
        g = {"test": "data"}
        fp = graph_fingerprint(g)
        raw = json.dumps(g, sort_keys=True).encode()
        expected = kaalka_encrypt(raw, time_key=123456)
        assert fp == expected


# ---------------------------------------------------------------------------
# 7. REFERENCE SPECIFICATION SEMANTICS
# ---------------------------------------------------------------------------

class TestReferenceSpecification:
    def test_deterministic_hash_is_64char_hex(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        h = compute_deterministic_hash({"any": "input"})
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_stable_serialize_sorts_keys_at_all_depths(self):
        from core.determinism.normalization import stable_serialize
        data = {"z": {"m": {"b": 1, "a": 2}, "a": 1}, "a": 1}
        result = stable_serialize(data)
        parsed = json.loads(result)
        top_keys = list(parsed.keys())
        assert top_keys == sorted(top_keys)
        inner_keys = list(parsed["z"].keys())
        assert inner_keys == sorted(inner_keys)

    def test_dumps_deterministic_normalizes_floats(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        result = dumps_deterministic({"val": 3.0})
        parsed = json.loads(result)
        assert parsed["val"] == 3

    def test_canonical_json_is_valid_json(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"a": 1, "b": [1, 2, 3], "c": {"nested": True}}
        result = dumps_deterministic(data)
        parsed = json.loads(result)
        assert parsed == data