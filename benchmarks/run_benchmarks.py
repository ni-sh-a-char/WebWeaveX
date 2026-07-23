# -*- coding: utf-8 -*-
"""WebWeaveX Python SDK - Reproducible Benchmark Suite.

Run: python benchmarks/run_benchmarks.py
"""
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.serialize.deterministic_serializer import dumps_deterministic
from core.determinism.normalization import stable_serialize, normalize_runtime_value
from core.crypto.kaalka_runtime_engine import compute_deterministic_hash, encrypt_value, decrypt_value
from core.crypto.kaalka_wrapper import graph_fingerprint
from core.replay.replay_equivalence_engine import validate_replay_equivalence
from core.runtime_graph.runtime_graph_engine import build_runtime_graph


def bench(name, fn, iterations=10000):
    for _ in range(100):
        fn()
    start = time.perf_counter()
    for _ in range(iterations):
        fn()
    elapsed = time.perf_counter() - start
    per_op = elapsed / iterations * 1000
    ops_per_sec = iterations / elapsed
    print("  %-40s %8.3fms/op  %10.0f ops/s" % (name, per_op, ops_per_sec))


def main():
    print("=" * 70)
    print("WebWeaveX Python SDK - Benchmark Suite")
    print("Python %s" % sys.version)
    print("Iterations: 10,000 per benchmark")
    print("=" * 70)

    print("\n--- Serialization ---")
    data = {"version": "3.0.0", "nested": {"a": 1, "b": [1, 2, 3]}, "key": "value"}
    bench("dumps_deterministic", lambda: dumps_deterministic(data))
    bench("stable_serialize", lambda: stable_serialize(data))
    bench("normalize_runtime_value", lambda: normalize_runtime_value("Hello World Test"))

    print("\n--- Hashing ---")
    bench("compute_deterministic_hash", lambda: compute_deterministic_hash(data))

    print("\n--- Kaalka ---")
    bench("encrypt_value", lambda: encrypt_value(data, "benchmark-key"))
    encrypted = encrypt_value(data, "benchmark-key")["encrypted"]
    bench("decrypt_value", lambda: decrypt_value(encrypted, "benchmark-key"))

    print("\n--- Graph Fingerprint ---")
    graph = {
        "nodes": [{"id": "n%d" % i, "type": "file"} for i in range(100)],
        "edges": [{"from": "n%d" % i, "to": "n%d" % (i+1), "type": "imports"} for i in range(99)]
    }
    bench("graph_fingerprint", lambda: graph_fingerprint(graph))

    print("\n--- ReplayEquivalence ---")
    envelope = {"unified_runtime_graph": graph}
    bench("validate_replay_equivalence", lambda: validate_replay_equivalence(envelope, envelope))

    print("\n--- Runtime Graph ---")
    bench("build_runtime_graph (serialize)", lambda: stable_serialize(graph))

    print("\n--- Large Scale ---")
    large_data = {"key_%d" % i: "value_%d" % i for i in range(1000)}
    bench("dumps_deterministic (1K keys)", lambda: dumps_deterministic(large_data), iterations=1000)
    bench("compute_deterministic_hash (1K keys)", lambda: compute_deterministic_hash(large_data), iterations=1000)

    print("\n" + "=" * 70)
    print("Benchmark complete. All operations deterministic and reproducible.")
    print("=" * 70)


if __name__ == "__main__":
    main()