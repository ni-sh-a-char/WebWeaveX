"""PYTHON-CERT-07: Independent Adversarial Audit.

Attempt to break every public API. Document every finding.
"""
import json
import pytest


class TestAdversarialSerialization:
    def test_empty_dict(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        assert dumps_deterministic({}) == "{}"

    def test_empty_list(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        assert dumps_deterministic([]) == "[]"

    def test_deeply_nested_100_levels(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        d = {}
        current = d
        for i in range(100):
            current["k"] = {}
            current = current["k"]
        assert isinstance(dumps_deterministic(d), str)

    def test_circular_reference_safe(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        d = {"a": 1}
        d["self"] = d
        try:
            dumps_deterministic(d)
        except (RecursionError, ValueError):
            pass  # Acceptable

    def test_enormous_string(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        assert len(dumps_deterministic({"text": "x" * 1_000_000})) > 1_000_000

    def test_all_none_values(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {f"k{i}": None for i in range(100)}
        parsed = json.loads(dumps_deterministic(data))
        assert all(v is None for v in parsed.values())

    def test_mixed_types(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"str": "a", "int": 1, "float": 1.5, "bool": True, "null": None, "list": [1], "dict": {"a": 1}}
        assert isinstance(json.loads(dumps_deterministic(data)), dict)


class TestAdversarialHashing:
    def test_empty_dict_hash(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        assert len(compute_deterministic_hash({})) == 64

    def test_hash_stability_50k(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        data = {"key": "value"}
        expected = compute_deterministic_hash(data)
        for _ in range(50000):
            assert compute_deterministic_hash(data) == expected

    def test_hash_large_payload(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        data = {f"key{i}": f"value{i}" for i in range(10000)}
        assert len(compute_deterministic_hash(data)) == 64


class TestAdversarialFingerprint:
    def test_empty_graph_fingerprint(self):
        from core.crypto.kaalka_wrapper import graph_fingerprint
        fp = graph_fingerprint({"nodes": [], "edges": []})
        assert isinstance(fp, bytes) and len(fp) > 0

    def test_graph_fingerprint_stability_50k(self):
        from core.crypto.kaalka_wrapper import graph_fingerprint
        g = {"nodes": [{"id": "n1"}], "edges": []}
        expected = graph_fingerprint(g)
        for _ in range(50000):
            assert graph_fingerprint(g) == expected


class TestAdversarialReplay:
    def test_empty_envelopes(self):
        from core.replay.replay_equivalence_engine import validate_replay_equivalence
        r = validate_replay_equivalence({}, {})
        assert r["equivalent"] is True

    def test_asymmetric_envelopes(self):
        from core.replay.replay_equivalence_engine import validate_replay_equivalence
        r = validate_replay_equivalence(
            {"graph": {"nodes": [{"id": "a"}], "edges": []}},
            {"graph": {"nodes": [{"id": "b"}], "edges": []}}
        )
        assert r["equivalent"] is False

    def test_replay_with_extra_keys(self):
        from core.replay.replay_equivalence_engine import validate_replay_equivalence
        r = validate_replay_equivalence(
            {"nodes": [{"id": "n1"}], "extra": "data"},
            {"nodes": [{"id": "n1"}]}
        )
        assert "equivalent" in r


class TestAdversarialNormalization:
    def test_empty_string(self):
        from core.determinism.normalization import normalize_runtime_value
        assert normalize_runtime_value("") == ""

    def test_only_whitespace(self):
        from core.determinism.normalization import normalize_runtime_value
        assert normalize_runtime_value("   ") == ""

    def test_null_bytes(self):
        from core.determinism.normalization import normalize_runtime_value
        assert "hello" in normalize_runtime_value("hello\x00world")

    def test_mixed_scripts(self):
        from core.determinism.normalization import normalize_runtime_value
        assert isinstance(normalize_runtime_value("hello world"), str)