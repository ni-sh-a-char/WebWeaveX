#!/usr/bin/env python3
"""Manifest governance validator for the Java port.

Fails (exit 1) on any of:
  1. a proven API not present in PARITY_MANIFEST.json,
  2. a mapped Java class file that does not exist,
  3. a proven API with no golden-vector section (untested),
  4. a proven API not documented in JAVA_PARITY_MATRIX.md,
  5. matrix/proven drift (matrix proven-count != mapping size).

Run from repo root:  python tools/validate_java_manifest.py
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVA = os.path.join(ROOT, "java")

# api -> (java class FQN, golden file, golden section key)
MAPPING = {
    "compute_kaalka_hash": ("io.webweavex.crypto.Kaalka", "golden_vectors.json", "crypto"),
    "encrypt_value": ("io.webweavex.crypto.Kaalka", "golden_vectors.json", "crypto"),
    "decrypt_value": ("io.webweavex.crypto.Kaalka", "golden_vectors.json", "crypto"),
    "UniversalInput": ("io.webweavex.kernel.UniversalInput", "golden_vectors_s2.json", "universal_input"),
    "build_runtime_graph": ("io.webweavex.graph.RuntimeGraph", "golden_vectors_s2.json", "graph"),
    "compile_unified_runtime_ir": ("io.webweavex.ir.UnifiedRuntimeIr", "golden_vectors_s2.json", "unified_ir"),
    "compute_global_runtime_fingerprint": ("io.webweavex.determinism.GlobalRuntimeFingerprint", "golden_vectors_s2.json", "global_fingerprint"),
    "fingerprint": ("io.webweavex.persistence.FingerprintHex", "golden_vectors_s2.json", None),
    "validate_replay_equivalence": ("io.webweavex.replay.ReplayEquivalence", "golden_vectors_s2.json", "replay"),
    "query_graph": ("io.webweavex.query.GraphQuery", "golden_vectors_s3.json", "query_graph"),
    "query_knowledge": ("io.webweavex.query.OntologyQuery", "golden_vectors_s3.json", "query_knowledge"),
    "query_runtime_graph": ("io.webweavex.query.GraphQuery", "golden_vectors_s3.json", "query_runtime_graph"),
    "build_runtime_memory": ("io.webweavex.memory.RuntimeMemory", "golden_vectors_s3.json", "build_runtime_memory"),
    "query_runtime_memory": ("io.webweavex.memory.MemoryQuery", "golden_vectors_s3.json", "query_runtime_memory"),
    "search_runtime_memory": ("io.webweavex.memory.MemorySearch", "golden_vectors_s3.json", "search_runtime_memory"),
    "reconstruct_runtime": ("io.webweavex.reconstruction.RuntimeReconstruction", "golden_vectors_s3.json", "reconstruct_runtime"),
    "validate_reconstructed_runtime": ("io.webweavex.reconstruction.RuntimeValidation", "golden_vectors_s3.json", "validate_reconstructed_runtime"),
    # fingerprint golden lives in s2 under the "fingerprint" section
}
MAPPING["fingerprint"] = ("io.webweavex.persistence.FingerprintHex", "golden_vectors_s2.json", "fingerprint")


def fail(errors):
    print("MANIFEST VALIDATION: FAIL")
    for e in errors:
        print("  -", e)
    sys.exit(1)


def main() -> None:
    errors = []
    manifest = json.load(open(os.path.join(ROOT, "PARITY_MANIFEST.json"), encoding="utf-8"))
    manifest_apis = {a["api"] for a in manifest["apis"]}

    golden_cache = {}

    def golden(fname):
        if fname not in golden_cache:
            path = os.path.join(JAVA, "src", "test", "resources", "parity", fname)
            golden_cache[fname] = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None
        return golden_cache[fname]

    matrix_path = os.path.join(JAVA, "JAVA_PARITY_MATRIX.md")
    matrix = open(matrix_path, encoding="utf-8").read() if os.path.exists(matrix_path) else ""
    matrix_proven = matrix.count("Implemented (parity-proven)")

    for api, (fqn, gfile, section) in MAPPING.items():
        # 1. in manifest
        if api not in manifest_apis:
            errors.append(f"{api}: not present in PARITY_MANIFEST.json")
        # 2. class file exists
        rel = os.path.join("src", "main", "java", *fqn.split(".")) + ".java"
        if not os.path.exists(os.path.join(JAVA, rel)):
            errors.append(f"{api}: mapped class {fqn} missing ({rel})")
        # 3. golden section present
        g = golden(gfile)
        if g is None:
            errors.append(f"{api}: golden file {gfile} missing")
        elif section is not None and section not in g:
            errors.append(f"{api}: golden section '{section}' absent in {gfile}")
        # 4. documented in matrix as proven
        if f"`{api}`" not in matrix:
            errors.append(f"{api}: not documented in JAVA_PARITY_MATRIX.md")

    # 5. matrix/mapping drift
    if matrix and matrix_proven != len(MAPPING):
        errors.append(
            f"matrix proven-count ({matrix_proven}) != mapping size ({len(MAPPING)}) — drift")

    if errors:
        fail(errors)
    print(f"MANIFEST VALIDATION: PASS — {len(MAPPING)}/{len(manifest_apis)} APIs proven, "
          f"all mapped/exist/tested/documented")


if __name__ == "__main__":
    main()
