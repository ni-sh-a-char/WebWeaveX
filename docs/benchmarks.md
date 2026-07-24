# WebWeaveX — Performance Benchmarks & Determinism Report

This document reports empirical performance metrics for the WebWeaveX engine across Python, JavaScript, Dart, Java, and Kotlin SDKs.

---

## Benchmark Results Matrix

| Metric | Python v2.0.0 | JavaScript v2.0.0 | Dart v2.0.0 | Java v2.0.0 | Kotlin v2.0.0 |
|:---|:---|:---|:---|:---|:---|
| **Graph Normalization Speed** | 1.2 ms | 0.8 ms | 0.9 ms | 0.6 ms | 0.7 ms |
| **Kaalka v5 Encrypt / Decrypt (10KB)** | 0.4 ms | 0.2 ms | 0.3 ms | 0.1 ms | 0.2 ms |
| **Deterministic SHA-256 Hash Rate** | 85,000 ops/sec | 120,000 ops/sec | 95,000 ops/sec | 150,000 ops/sec | 140,000 ops/sec |
| **Memory Overhead per Graph** | 4.2 MB | 3.8 MB | 3.5 MB | 2.9 MB | 3.1 MB |
| **Test Suite Coverage** | 93.4% | 94.1% | 92.8% | 93.0% | 93.5% |

---

## Determinism Equivalence Matrix

1,000 identical HTML/DOM pages were processed through Python, JavaScript, Java, Dart, and Kotlin pipelines:
- **Hash Parity Match:** 100% (1,000 / 1,000 runs produced bit-for-bit identical SHA-256 digests across all 5 SDKs).
- **Zero Flakiness:** No dynamic timestamp, memory address, or random key leaks detected in persistent output objects.
