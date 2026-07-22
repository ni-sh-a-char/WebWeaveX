"""PYTHON-CERT-03: Determinism Certification Tests.

Proves that every deterministic subsystem produces identical output
across thousands of iterations.
"""
import json
import pytest


class TestSerializationDeterminism:
    def test_dumps_deterministic_1000_iterations(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"z": 1, "a": 2, "nested": {"b": 3, "a": 1}, "list": [3, 1, 2]}
        expected = dumps_deterministic(data)
        for _ in range(1000):
            assert dumps_deterministic(data) == expected

    def test_dumps_canonical_v5_1000_iterations(self):
        from core.serialize.deterministic_serializer import dumps_canonical_v5
        data = {"version": "3.0.0", "nested": {"x": True, "y": None}}
        expected = dumps_canonical_v5(data)
        for _ in range(1000):
            assert dumps_canonical_v5(data) == expected

    def test_sorted_keys(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"z": 1, "a": 2, "m": 3}
        result = dumps_deterministic(data)
        keys = json.loads(result).keys()
        assert list(keys) == ["a", "m", "z"]

    def test_golden_serialization(self):
        from core.serialize.deterministic_serializer import dumps_deterministic
        data = {"a": 1, "b": 2, "c": 3}
        assert dumps_deterministic(data) == '{"a":1,"b":2,"c":3}'


class TestNormalizationDeterminism:
    def test_stable_serialize_1000_iterations(self):
        from core.determinism.normalization import stable_serialize
        data = {"b": 2, "a": 1, "nested": {"z": 3, "a": 1}}
        expected = stable_serialize(data)
        for _ in range(1000):
            assert stable_serialize(data) == expected

    def test_normalize_runtime_value_deterministic(self):
        from core.determinism.normalization import normalize_runtime_value
        for v in ["Hello World", "  spaced  ", "cafe", ""]:
            expected = normalize_runtime_value(v)
            for _ in range(1000):
                assert normalize_runtime_value(v) == expected

    def test_stable_sort_keys_deterministic(self):
        from core.determinism.normalization import stable_sort_keys
        data = {"z": 1, "a": 2, "m": 3, "b": 4}
        expected = stable_sort_keys(data)
        for _ in range(1000):
            assert stable_sort_keys(data) == expected

    def test_golden_normalization(self):
        from core.determinism.normalization import stable_serialize
        data = {"z": 1, "a": 2}
        result = stable_serialize(data)
        assert '"a":2' in result and '"z":1' in result
        assert result.index('"a"') < result.index('"z"')


class TestHashingDeterminism:
    def test_compute_deterministic_hash_1000_iterations(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        data = {"key": "value", "number": 42, "nested": {"a": 1}}
        expected = compute_deterministic_hash(data)
        for _ in range(1000):
            assert compute_deterministic_hash(data) == expected

    def test_hash_is_64_char_hex(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        h = compute_deterministic_hash({"test": "data"})
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_hash_different_for_different_inputs(self):
        from core.crypto.kaalka_runtime_engine import compute_deterministic_hash
        assert compute_deterministic_hash({"a": 1}) != compute_deterministic_hash({"a": 2})


class TestFingerprintDeterminism:
    def test_graph_fingerprint_deterministic(self):
        from core.crypto.kaalka_wrapper import graph_fingerprint
        graph = {
            "nodes": [{"id": "n1", "type": "file"}, {"id": "n2", "type": "module"}],
            "edges": [{"from": "n1", "to": "n2", "type": "imports"}],
        }
        expected = graph_fingerprint(graph)
        for _ in range(1000):
            assert graph_fingerprint(graph) == expected

    def test_graph_fingerprint_keys_sorted(self):
        from core.crypto.kaalka_wrapper import graph_fingerprint
        assert graph_fingerprint({"z": 1, "a": 2}) == graph_fingerprint({"a": 2, "z": 1})


class TestReplayDeterminism:
    def test_validate_replay_equivalence_1000_iterations(self):
        from core.replay.replay_equivalence_engine import validate_replay_equivalence
        original = {"nodes": [{"id": "n1"}], "edges": []}
        replayed = {"nodes": [{"id": "n1"}], "edges": []}
        expected = validate_replay_equivalence(original, replayed)
        for _ in range(1000):
            assert validate_replay_equivalence(original, replayed) == expected


class TestRuntimeGraphDeterminism:
    def test_build_runtime_graph_deterministic(self):
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph
        data = [{"ir": "test", "nodes": [{"id": "n1", "type": "file"}], "edges": []}]
        g1 = build_runtime_graph(data)
        g2 = build_runtime_graph(data)
        assert json.dumps(g1, sort_keys=True) == json.dumps(g2, sort_keys=True)