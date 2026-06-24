#!/usr/bin/env python3
"""Manifest + branch-identity governance validator for the Java port.

Fails (exit 1) on any of:

  Manifest / parity integrity (original checks):
    1.  a proven API not present in PARITY_MANIFEST.json,
    2.  a mapped Java class file that does not exist,
    3.  a proven API with no golden-vector section (untested),
    4.  a proven API not documented in JAVA_PARITY_MATRIX.md,
    5.  matrix/mapping drift (matrix proven-count != mapping size).

  Branch identity (Maven-first; added Phase 4):
    6.  README references a foreign ecosystem's install/badge surface
        (pub.dev/Dart badges, npm installation, pip installation).
    7.  an implemented Java package is undocumented (absent from the matrix).
    8.  a proven API has no parity test that loads its golden-vector file.
    9.  a proven API has no matrix *entry* (covered by 4) — kept explicit.
    10. source drift: a mapped Java class with no matrix proven-row, OR a matrix
        proven-row whose API is not mapped to a source class (bidirectional).

Run from repo root:  python tools/validate_java_manifest.py
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVA = os.path.join(ROOT, "java")
PARITY_DIR = os.path.join(JAVA, "src", "test", "resources", "parity")
TEST_DIR = os.path.join(JAVA, "src", "test", "java")

# api -> (java class FQN, golden file, golden section key)
MAPPING = {
    "compute_kaalka_hash": ("io.webweavex.crypto.Kaalka", "golden_vectors.json", "crypto"),
    "encrypt_value": ("io.webweavex.crypto.Kaalka", "golden_vectors.json", "crypto"),
    "decrypt_value": ("io.webweavex.crypto.Kaalka", "golden_vectors.json", "crypto"),
    "UniversalInput": ("io.webweavex.kernel.UniversalInput", "golden_vectors_s2.json", "universal_input"),
    "build_runtime_graph": ("io.webweavex.graph.RuntimeGraph", "golden_vectors_s2.json", "graph"),
    "compile_unified_runtime_ir": ("io.webweavex.ir.UnifiedRuntimeIr", "golden_vectors_s2.json", "unified_ir"),
    "compute_global_runtime_fingerprint": ("io.webweavex.determinism.GlobalRuntimeFingerprint", "golden_vectors_s2.json", "global_fingerprint"),
    "fingerprint": ("io.webweavex.persistence.FingerprintHex", "golden_vectors_s2.json", "fingerprint"),
    "validate_replay_equivalence": ("io.webweavex.replay.ReplayEquivalence", "golden_vectors_s2.json", "replay"),
    "query_graph": ("io.webweavex.query.GraphQuery", "golden_vectors_s3.json", "query_graph"),
    "query_knowledge": ("io.webweavex.query.OntologyQuery", "golden_vectors_s3.json", "query_knowledge"),
    "query_runtime_graph": ("io.webweavex.query.GraphQuery", "golden_vectors_s3.json", "query_runtime_graph"),
    "build_runtime_memory": ("io.webweavex.memory.RuntimeMemory", "golden_vectors_s3.json", "build_runtime_memory"),
    "query_runtime_memory": ("io.webweavex.memory.MemoryQuery", "golden_vectors_s3.json", "query_runtime_memory"),
    "search_runtime_memory": ("io.webweavex.memory.MemorySearch", "golden_vectors_s3.json", "search_runtime_memory"),
    "reconstruct_runtime": ("io.webweavex.reconstruction.RuntimeReconstruction", "golden_vectors_s3.json", "reconstruct_runtime"),
    "validate_reconstructed_runtime": ("io.webweavex.reconstruction.RuntimeValidation", "golden_vectors_s3.json", "validate_reconstructed_runtime"),
    # Session 4 — connector-runtime extraction (deterministic Extraction layer)
    "extract_database_runtime": ("io.webweavex.connectors.DatabaseConnectors", "golden_vectors_s4.json", "extract_database_runtime"),
    "extract_api_runtime": ("io.webweavex.connectors.ApiConnectors", "golden_vectors_s4.json", "extract_api_runtime"),
    "extract_runtime_streams": ("io.webweavex.connectors.StreamConnectors", "golden_vectors_s4.json", "extract_runtime_streams"),
    "extract_telemetry_runtime": ("io.webweavex.connectors.TelemetryConnector", "golden_vectors_s4.json", "extract_telemetry_runtime"),
    # Session 4B — pure document + pagination extraction (dependency-proof survivors)
    "extract_document_runtime": ("io.webweavex.documents.DocumentRuntime", "golden_vectors_s4b.json", "extract_document_runtime"),
    "extract_paginated_content": ("io.webweavex.interaction.Pagination", "golden_vectors_s4b.json", "extract_paginated_content"),
    # Session 6 — interaction graph (dependency-clean)
    "build_interaction_graph": ("io.webweavex.interaction.InteractionGraph", "golden_vectors_s6.json", "build_interaction_graph"),
    # Session 7 — remaining connector-runtime cluster (dependency-clean)
    "extract_container_runtime": ("io.webweavex.connectors.ContainerConnector", "golden_vectors_s7.json", "extract_container_runtime"),
    "extract_ide_runtime": ("io.webweavex.connectors.IdeConnector", "golden_vectors_s7.json", "extract_ide_runtime"),
    "extract_kubernetes_runtime": ("io.webweavex.connectors.KubernetesConnector", "golden_vectors_s7.json", "extract_kubernetes_runtime"),
    # Session 8 — session-crypto cluster + json.loads substrate
    "encrypt_session_state": ("io.webweavex.crypto.KaalkaSession", "golden_vectors_s8.json", "encrypt_session_state"),
    "decrypt_session_state": ("io.webweavex.crypto.KaalkaSession", "golden_vectors_s8.json", "decrypt_session_state"),
    "save_encrypted_session": ("io.webweavex.session.EncryptedSessionStore", "golden_vectors_s8.json", "save_encrypted_session"),
    "load_encrypted_session": ("io.webweavex.session.EncryptedSessionStore", "golden_vectors_s8.json", "load_encrypted_session"),
    # Session 9 — execution family (dependency-clean, 26-module closure)
    "build_runtime_sandbox": ("io.webweavex.execution.ExecutionRuntime", "golden_vectors_s9.json", "build_runtime_sandbox"),
    "execute_runtime_action": ("io.webweavex.execution.ExecutionRuntime", "golden_vectors_s9.json", "execute_runtime_action"),
    "replay_runtime_execution": ("io.webweavex.execution.ExecutionRuntime", "golden_vectors_s9.json", "replay_runtime_execution"),
    "simulate_runtime_execution": ("io.webweavex.execution.ExecutionRuntime", "golden_vectors_s9.json", "simulate_runtime_execution"),
    "run_execution_runtime": ("io.webweavex.execution.ExecutionRuntime", "golden_vectors_s9.json", "run_execution_runtime"),
    "run_execution_for_extraction": ("io.webweavex.execution.ExecutionRuntime", "golden_vectors_s9.json", "run_execution_for_extraction"),
    # Session 10 — synchronization family (dependency-clean, 25-module closure)
    "build_runtime_delta": ("io.webweavex.synchronization.SyncRuntime", "golden_vectors_s10.json", "build_runtime_delta"),
    "replay_synchronized_runtime": ("io.webweavex.synchronization.SyncRuntime", "golden_vectors_s10.json", "replay_synchronized_runtime"),
    "run_synchronized_runtime": ("io.webweavex.synchronization.SyncRuntime", "golden_vectors_s10.json", "run_synchronized_runtime"),
    "run_sync_for_extraction": ("io.webweavex.synchronization.SyncRuntime", "golden_vectors_s10.json", "run_sync_for_extraction"),
    "save_sync_memory": ("io.webweavex.synchronization.SyncRuntime", "golden_vectors_s10.json", "save_sync_memory"),
    "load_sync_memory": ("io.webweavex.synchronization.SyncRuntime", "golden_vectors_s10.json", "load_sync_memory"),
    # Session 11 — workflows family (dependency-clean, 23-module closure)
    "build_runtime_objective": ("io.webweavex.workflow.WorkflowRuntime", "golden_vectors_s11.json", "build_runtime_objective"),
    "build_workflow_plan": ("io.webweavex.workflow.WorkflowRuntime", "golden_vectors_s11.json", "build_workflow_plan"),
    "run_autonomous_workflow": ("io.webweavex.workflow.WorkflowRuntime", "golden_vectors_s11.json", "run_autonomous_workflow"),
    "replay_workflow_runtime": ("io.webweavex.workflow.WorkflowRuntime", "golden_vectors_s11.json", "replay_workflow_runtime"),
    "run_workflow_for_extraction": ("io.webweavex.workflow.WorkflowRuntime", "golden_vectors_s11.json", "run_workflow_for_extraction"),
    "save_workflow_memory": ("io.webweavex.workflow.WorkflowRuntime", "golden_vectors_s11.json", "save_workflow_memory"),
    "load_workflow_memory": ("io.webweavex.workflow.WorkflowRuntime", "golden_vectors_s11.json", "load_workflow_memory"),
    # Session 12 — evolution_runtime family (dependency-clean, 25-module closure)
    "build_runtime_evolution": ("io.webweavex.evolution.EvolutionRuntime", "golden_vectors_s12.json", "build_runtime_evolution"),
    "evolve_selector_runtime": ("io.webweavex.evolution.EvolutionRuntime", "golden_vectors_s12.json", "evolve_selector_runtime"),
    "run_evolution_runtime": ("io.webweavex.evolution.EvolutionRuntime", "golden_vectors_s12.json", "run_evolution_runtime"),
    "run_evolution_for_extraction": ("io.webweavex.evolution.EvolutionRuntime", "golden_vectors_s12.json", "run_evolution_for_extraction"),
    "save_evolution_runtime": ("io.webweavex.evolution.EvolutionRuntime", "golden_vectors_s12.json", "save_evolution_runtime"),
    "load_evolution_runtime": ("io.webweavex.evolution.EvolutionRuntime", "golden_vectors_s12.json", "load_evolution_runtime"),
    # Session 13 — causality family (dependency-clean, 25-module closure)
    "run_causality_runtime": ("io.webweavex.causality.CausalityRuntime", "golden_vectors_s13.json", "run_causality_runtime"),
    "replay_causal_runtime": ("io.webweavex.causality.CausalityRuntime", "golden_vectors_s13.json", "replay_causal_runtime"),
    "run_causality_for_extraction": ("io.webweavex.causality.CausalityRuntime", "golden_vectors_s13.json", "run_causality_for_extraction"),
    "save_causal_memory": ("io.webweavex.causality.CausalityRuntime", "golden_vectors_s13.json", "save_causal_memory"),
    "load_causal_memory": ("io.webweavex.causality.CausalityRuntime", "golden_vectors_s13.json", "load_causal_memory"),
    # Session 14 — streaming + live_runtime family (dependency-clean)
    "build_stream_timeline": ("io.webweavex.streaming.StreamingRuntime", "golden_vectors_s14.json", "build_stream_timeline"),
    "replay_stream_events": ("io.webweavex.streaming.StreamingRuntime", "golden_vectors_s14.json", "replay_stream_events"),
    "run_live_runtime": ("io.webweavex.streaming.StreamingRuntime", "golden_vectors_s14.json", "run_live_runtime"),
    "save_live_runtime": ("io.webweavex.streaming.StreamingRuntime", "golden_vectors_s14.json", "save_live_runtime"),
    "load_live_runtime": ("io.webweavex.streaming.StreamingRuntime", "golden_vectors_s14.json", "load_live_runtime"),
    # Session 15 — adaptive modal recovery (dependency-clean, 1 module)
    "recover_modal_runtime": ("io.webweavex.adaptive.ModalRecovery", "golden_vectors_s15.json", "recover_modal_runtime"),
    # Session 16 — reconstruction orchestrator (dependency-clean, 24-module closure)
    "run_reconstruction_runtime": ("io.webweavex.reconstruction.ReconstructionRuntime", "golden_vectors_s16.json", "run_reconstruction_runtime"),
    "run_reconstruction_for_extraction": ("io.webweavex.reconstruction.ReconstructionRuntime", "golden_vectors_s16.json", "run_reconstruction_for_extraction"),
    # Session 17 — memory persistence x4 (dependency-clean)
    "save_runtime_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "save_runtime_memory"),
    "load_runtime_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "load_runtime_memory"),
    "save_semantic_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "save_semantic_memory"),
    "load_semantic_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "load_semantic_memory"),
    "save_adaptive_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "save_adaptive_memory"),
    "load_adaptive_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "load_adaptive_memory"),
    "save_application_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "save_application_memory"),
    "load_application_memory": ("io.webweavex.memory.MemoryPersistence", "golden_vectors_s17.json", "load_application_memory"),
    # Session 18 — browser identity (dependency-clean, 28-module closure)
    "build_browser_identity": ("io.webweavex.identity.IdentityRuntime", "golden_vectors_s18.json", "build_browser_identity"),
    "save_browser_identity": ("io.webweavex.identity.IdentityRuntime", "golden_vectors_s18.json", "save_browser_identity"),
    "load_browser_identity": ("io.webweavex.identity.IdentityRuntime", "golden_vectors_s18.json", "load_browser_identity"),
    # Session 19 — clean remainder slice
    "save_distributed_checkpoint": ("io.webweavex.distributed.DistributedCheckpoint", "golden_vectors_s19.json", "save_distributed_checkpoint"),
    "load_distributed_checkpoint": ("io.webweavex.distributed.DistributedCheckpoint", "golden_vectors_s19.json", "load_distributed_checkpoint"),
    "save_native_runtime": ("io.webweavex.memory.NativeRuntimePersistence", "golden_vectors_s19.json", "save_native_runtime"),
    "load_native_runtime": ("io.webweavex.memory.NativeRuntimePersistence", "golden_vectors_s19.json", "load_native_runtime"),
    "replay_semantic_runtime": ("io.webweavex.semantic.SemanticReplay", "golden_vectors_s19.json", "replay_semantic_runtime"),
    "execute_runtime_objective": ("io.webweavex.application.ObjectiveExecution", "golden_vectors_s19.json", "execute_runtime_objective"),
    "query_repository": ("io.webweavex.repository.RepositoryQuery", "golden_vectors_s19.json", "query_repository"),
    "authenticate_runtime": ("io.webweavex.auth.AuthenticationRuntime", "golden_vectors_s19.json", "authenticate_runtime"),
    "clone_runtime_environment": ("io.webweavex.reconstruction.ReconstructionRuntime", "golden_vectors_s16.json", "clone_runtime_environment"),
    "fabricate_runtime_reality": ("io.webweavex.reconstruction.ReconstructionRuntime", "golden_vectors_s16.json", "fabricate_runtime_reality"),
    # Session 20 — memory orchestrator (final clean slice)
    "run_runtime_memory": ("io.webweavex.memory.RuntimeMemoryRuntime", "golden_vectors_s20.json", "run_runtime_memory"),
    "run_memory_for_extraction": ("io.webweavex.memory.RuntimeMemoryRuntime", "golden_vectors_s20.json", "run_memory_for_extraction"),
    # Session 21 — Tier-B start: heal_selector portable (empty-HTML) contract
    "heal_selector": ("io.webweavex.adaptive.SelectorHealing", "golden_vectors_s21.json", "heal_selector"),
    # Session 22 — Tier-B1: query_documents (pure document semantic IR)
    "query_documents": ("io.webweavex.documents.DocumentSemanticIr", "golden_vectors_s22.json", "query_documents"),
    # Session 25 — semantic runtime (portable html="" contract)
    "run_semantic_runtime": ("io.webweavex.semantic.SemanticRuntime", "golden_vectors_s25.json", "run_semantic_runtime"),
    "run_semantic_for_extraction": ("io.webweavex.semantic.SemanticRuntime", "golden_vectors_s25.json", "run_semantic_for_extraction"),
    # Session 26 — application cognition (portable html="" contract)
    "run_application_cognition": ("io.webweavex.application.ApplicationCognitionRuntime", "golden_vectors_s26.json", "run_application_cognition"),
    # Session 28 — frontier-reduced portable APIs (constants, passthrough, reuse, stub-page engines)
    "version": ("io.webweavex.WebWeaveX", "golden_vectors_s28.json", "version"),
    "__version__": ("io.webweavex.WebWeaveX", "golden_vectors_s28.json", "__version__"),
    "query_repo": ("io.webweavex.repository.RepositoryQuery", "golden_vectors_s28.json", "query_repo"),
    "compile_document": ("io.webweavex.documents.DocumentSemanticIr", "golden_vectors_s28.json", "compile_document"),
    "capture_websocket_frames": ("io.webweavex.streaming.StreamingRuntime", "golden_vectors_s28.json", "capture_websocket_frames"),
    "capture_dom_mutations": ("io.webweavex.streaming.StreamingRuntime", "golden_vectors_s28.json", "capture_dom_mutations"),
    "extract_infinite_scroll": ("io.webweavex.interaction.InfiniteScroll", "golden_vectors_s28.json", "extract_infinite_scroll"),
    "replay_interactions": ("io.webweavex.interaction.InteractionReplay", "golden_vectors_s28.json", "replay_interactions"),
    # Session 30 — PORT-APPROVED aggregators certified (kernel + distributed scheduler)
    "RuntimeKernel": ("io.webweavex.kernel.RuntimeKernel", "golden_vectors_s30.json", "RuntimeKernel"),
    "get_runtime_kernel": ("io.webweavex.kernel.RuntimeKernel", "golden_vectors_s30.json", "get_runtime_kernel"),
    "run_autonomous_extraction": ("io.webweavex.distributed.AutonomousExtraction", "golden_vectors_s30.json", "run_autonomous_extraction"),
}

PROVEN_MARK = "Implemented (parity-proven)"

# Foreign-ecosystem install/badge patterns forbidden in the Java README. These
# target install *commands* and *badge URLs*, NOT bare ecosystem names — the
# parity/branch table legitimately names Python, npm, pub.dev, and PyPI.
README_FORBIDDEN = [
    (r"img\.shields\.io/pub", "pub.dev version badge"),
    (r"shields\.io/badge/Dart", "Dart language badge"),
    (r"\bdart\s+pub\s+(add|get|publish)\b", "Dart pub install/publish command"),
    (r"pub\.dev/packages", "pub.dev package link"),
    (r"\bpubspec\b", "pubspec (Dart manifest) reference"),
    (r"\bnpm\s+(install|i|add)\b", "npm installation command"),
    (r"\bpip\s+install\b", "pip installation command"),
]


def fail(errors):
    print("MANIFEST VALIDATION: FAIL")
    for e in errors:
        print("  -", e)
    sys.exit(1)


def read(path):
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def proven_apis_in_matrix(matrix: str) -> set[str]:
    """APIs whose matrix row is marked Implemented (parity-proven).

    Matrix rows look like: ``| `api_name` | ... | ✅ Implemented (parity-proven) |``.
    """
    found = set()
    for line in matrix.splitlines():
        if PROVEN_MARK not in line:
            continue
        m = re.search(r"\|\s*`([^`]+)`", line)
        if m:
            found.add(m.group(1))
    return found


def main() -> None:
    errors = []
    manifest = json.load(open(os.path.join(ROOT, "PARITY_MANIFEST.json"), encoding="utf-8"))
    manifest_apis = {a["api"] for a in manifest["apis"]}

    golden_cache = {}

    def golden(fname):
        if fname not in golden_cache:
            path = os.path.join(PARITY_DIR, fname)
            golden_cache[fname] = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None
        return golden_cache[fname]

    matrix = read(os.path.join(JAVA, "JAVA_PARITY_MATRIX.md"))
    matrix_proven = matrix.count(PROVEN_MARK)

    # Concatenate all parity test sources once (check 8).
    test_blob = ""
    if os.path.isdir(TEST_DIR):
        for dirpath, _dirs, names in os.walk(TEST_DIR):
            for n in names:
                if n.endswith(".java"):
                    test_blob += read(os.path.join(dirpath, n))

    for api, (fqn, gfile, section) in MAPPING.items():
        # 1. in manifest
        if api not in manifest_apis:
            errors.append(f"{api}: not present in PARITY_MANIFEST.json")
        # 2. class file exists (source present)
        rel = os.path.join("src", "main", "java", *fqn.split(".")) + ".java"
        if not os.path.exists(os.path.join(JAVA, rel)):
            errors.append(f"{api}: mapped class {fqn} missing ({rel})")
        # 3. golden section present (tested data)
        g = golden(gfile)
        if g is None:
            errors.append(f"{api}: golden file {gfile} missing")
        elif section is not None and section not in g:
            errors.append(f"{api}: golden section '{section}' absent in {gfile}")
        # 4/9. documented in matrix as proven
        if f"`{api}`" not in matrix:
            errors.append(f"{api}: not documented in JAVA_PARITY_MATRIX.md (check 4/9)")
        # 7. implemented package documented in matrix
        pkg = fqn.rsplit(".", 1)[0]
        if pkg not in matrix:
            errors.append(f"{api}: package {pkg} undocumented in JAVA_PARITY_MATRIX.md (check 7)")
        # 8. a parity test loads this api's golden file
        if test_blob and gfile not in test_blob:
            errors.append(f"{api}: no parity test references golden file {gfile} (check 8)")

    # 5. matrix/mapping drift
    if matrix and matrix_proven != len(MAPPING):
        errors.append(
            f"matrix proven-count ({matrix_proven}) != mapping size ({len(MAPPING)}) — drift (check 5)")

    # 10. bidirectional source<->matrix drift
    if matrix:
        matrix_proven_apis = proven_apis_in_matrix(matrix)
        mapping_apis = set(MAPPING)
        for api in mapping_apis - matrix_proven_apis:
            errors.append(f"{api}: mapped to a source class but no proven matrix row (check 10)")
        for api in matrix_proven_apis - mapping_apis:
            errors.append(f"{api}: proven matrix row but no source mapping (check 10)")

    # 6. README foreign-ecosystem install/badge surface
    readme = read(os.path.join(ROOT, "README.md"))
    if not readme:
        errors.append("README.md missing (check 6)")
    else:
        for pat, label in README_FORBIDDEN:
            if re.search(pat, readme, re.IGNORECASE):
                errors.append(f"README references foreign ecosystem: {label} (/{pat}/) (check 6)")

    if errors:
        fail(errors)
    print(f"MANIFEST VALIDATION: PASS — {len(MAPPING)}/{len(manifest_apis)} APIs proven; "
          f"mapped/exist/tested/documented; README Java-native; source<->matrix consistent")


if __name__ == "__main__":
    main()
