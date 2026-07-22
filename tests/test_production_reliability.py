"""PYTHON-CERT-04: Production Reliability Certification.

Stress tests, error resilience, and long-run stability for the
reference runtime.
"""
import gc
import json
import pytest


class TestLargeScaleWorkloads:
    def test_10000_serializations(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"nodes": [{"id": f"n{i}", "type": "file", "name": f"file_{i}.py"} for i in range(100)],
                "edges": [{"from": f"n{i}", "to": f"n{i+1}", "type": "imports"} for i in range(99)]}
        for i in range(10000):
            assert isinstance(dumps_deterministic(data), str)

    def test_10000_fingerprints(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        data = {"version": "3.0.0", "nodes": list(range(100))}
        expected = compute_deterministic_hash(data)
        for _ in range(10000):
            assert compute_deterministic_hash(data) == expected

    def test_10000_graph_fingerprints(self):
        from core.crypto.kaalka_wrapper import graph_fingerprint
        graph = {"nodes": [{"id": f"n{i}", "type": "t"} for i in range(50)],
                 "edges": [{"from": f"n{i}", "to": f"n{i+1}"} for i in range(49)]}
        expected = graph_fingerprint(graph)
        for _ in range(10000):
            assert graph_fingerprint(graph) == expected

    def test_10000_replay_validations(self):
        from core.replay.replay_equivalence_engine import validate_replay_equivalence
        original = {"nodes": [{"id": f"n{i}"} for i in range(100)],
                    "edges": [{"from": f"n{i}", "to": f"n{i+1}"} for i in range(99)]}
        for _ in range(10000):
            result = validate_replay_equivalence(original, original)
            assert result is not None

    def test_10000_runtime_graph_builds(self):
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph
        for _ in range(10000):
            data = [{"ir": "test", "nodes": [{"id": "n1", "type": "file"}], "edges": []}]
            g = build_runtime_graph(data)
            assert isinstance(g, dict)

    def test_10000_stable_serializations(self):
        from core.determinism.normalization import stable_serialize
        data = {"z": 1, "a": 2, "nested": {"m": 3, "b": 4}}
        expected = stable_serialize(data)
        for _ in range(10000):
            assert stable_serialize(data) == expected


class TestLongRunStability:
    def test_deterministic_output_stability(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        from core.determinism.normalization import stable_serialize
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        for i in range(5000):
            data = {"iteration": i, "data": f"payload_{i % 100}"}
            assert dumps_deterministic(data) == dumps_deterministic(data)
            assert stable_serialize(data) == stable_serialize(data)
            assert compute_deterministic_hash(data) == compute_deterministic_hash(data)

    def test_no_state_leakage_between_calls(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        from core.determinism.normalization import stable_serialize
        for i in range(1000):
            assert dumps_deterministic({"a": i}) != dumps_deterministic({"a": i + 1})
            assert stable_serialize({"x": i}) != stable_serialize({"x": i + 1})

    def test_memory_stability_under_repetition(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        gc.collect()
        initial = len(gc.get_objects())
        for _ in range(5000):
            compute_deterministic_hash({"key": "value", "nested": {"a": list(range(100))}})
        gc.collect()
        final = len(gc.get_objects())
        assert final < initial * 1.5, f"Memory grew: {initial} -> {final}"


class TestErrorResilience:
    def test_empty_graph(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        assert dumps_deterministic({}) == "{}"
        assert dumps_deterministic([]) == "[]"

    def test_deeply_nested_structure(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        nested = {"level": 0}
        current = nested
        for i in range(1, 100):
            current["child"] = {"level": i}
            current = current["child"]
        assert isinstance(dumps_deterministic(nested), str)

    def test_unicode_handling(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        from core.determinism.normalization import normalize_runtime_value
        data = {"text": "Hello \u4e16\u754c \u00e9\u00e8\u00ea \u0639\u0631\u0628\u064a"}
        assert isinstance(dumps_deterministic(data), str)
        assert normalize_runtime_value("\u00e9\u00e8\u00ea") is not None

    def test_null_values(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"a": None, "b": 0, "c": False, "d": ""}
        parsed = json.loads(dumps_deterministic(data))
        assert parsed["a"] is None
        assert parsed["b"] == 0
        assert parsed["c"] is False
        assert parsed["d"] == ""

    def test_large_strings(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"text": "x" * 100000}
        assert len(dumps_deterministic(data)) > 100000

    def test_empty_replay_equivalence(self):
        from core.replay.replay_equivalence_engine import validate_replay_equivalence
        result = validate_replay_equivalence({}, {})
        assert result is not None
        assert result.get("equivalent") is True

    def test_float_normalization(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"pi": 3.14159265358979, "small": 1e-10, "large": 1e20}
        parsed = json.loads(dumps_deterministic(data))
        assert isinstance(parsed["pi"], float)
        assert isinstance(parsed["small"], float)

    def test_repeated_same_input(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        results = set(dumps_deterministic({"same": "input"}) for _ in range(100))
        assert len(results) == 1


class TestSerializationChain:
    def test_dumps_deterministic_to_stable_serialize_consistency(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        from core.determinism.normalization import stable_serialize
        data = {"b": 2, "a": 1}
        d1 = json.loads(dumps_deterministic(data))
        d2 = json.loads(stable_serialize(data))
        assert d1 == d2
        assert list(d1.keys()) == ["a", "b"]

    def test_hash_after_serialization_deterministic(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        data = {"key": "value"}
        h1 = compute_deterministic_hash(json.loads(dumps_deterministic(data)))
        h2 = compute_deterministic_hash(json.loads(dumps_deterministic(data)))
        assert h1 == h2

    def test_fingerprint_after_serialization_deterministic(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        from core.crypto.kaalka_wrapper import graph_fingerprint
        graph = {"nodes": [{"id": "n1"}], "edges": []}
        fp1 = graph_fingerprint(graph)
        fp2 = graph_fingerprint(json.loads(dumps_deterministic(graph)))
        assert fp1 == fp2