#!/usr/bin/env python3
"""Generate java/JAVA_PARITY_MATRIX.md from PARITY_MANIFEST.json.

The matrix is manifest-generated (no hand-maintained counts) so it can never
drift from the single source of truth. The Java column reflects what is actually
implemented and parity-proven in the java/ branch today.
"""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "PARITY_MANIFEST.json")
OUT = os.path.join(ROOT, "java", "JAVA_PARITY_MATRIX.md")

# Public manifest APIs implemented AND cross-language parity-proven in this
# foundation slice (see CrossLanguageParityTest — 80 byte-exact assertions).
JAVA_PROVEN = {
    # Session 1 — determinism + crypto foundation
    "compute_kaalka_hash": "io.webweavex.crypto.Kaalka#computeKaalkaHash",
    "encrypt_value": "io.webweavex.crypto.Kaalka#encryptValue",
    "decrypt_value": "io.webweavex.crypto.Kaalka#decryptValue",
    # Session 2 — kernel / graph / ir / persistence / fingerprint / replay
    "UniversalInput": "io.webweavex.kernel.UniversalInput",
    "build_runtime_graph": "io.webweavex.graph.RuntimeGraph#buildParityRuntimeGraph",
    "compile_unified_runtime_ir": "io.webweavex.ir.UnifiedRuntimeIr#compile",
    "compute_global_runtime_fingerprint": "io.webweavex.determinism.GlobalRuntimeFingerprint#compute",
    "fingerprint": "io.webweavex.persistence.FingerprintHex#fingerprint",
    "validate_replay_equivalence": "io.webweavex.replay.ReplayEquivalence#validate",
    # Session 3 — query / memory / reconstruction
    "query_graph": "io.webweavex.query.GraphQuery#queryGraph",
    "query_knowledge": "io.webweavex.query.OntologyQuery#queryKnowledge",
    "query_runtime_graph": "io.webweavex.query.GraphQuery#queryRuntimeGraph",
    "build_runtime_memory": "io.webweavex.memory.RuntimeMemory#build",
    "query_runtime_memory": "io.webweavex.memory.MemoryQuery#queryRuntimeMemory",
    "search_runtime_memory": "io.webweavex.memory.MemorySearch#searchRuntimeMemory",
    "reconstruct_runtime": "io.webweavex.reconstruction.RuntimeReconstruction#reconstructRuntime",
    "validate_reconstructed_runtime": "io.webweavex.reconstruction.RuntimeValidation#validateReconstructedRuntime",
    # Session 4 — connector-runtime extraction (deterministic Extraction layer)
    "extract_database_runtime": "io.webweavex.connectors.DatabaseConnectors#extractDatabaseRuntime",
    "extract_api_runtime": "io.webweavex.connectors.ApiConnectors#extractApiRuntime",
    "extract_runtime_streams": "io.webweavex.connectors.StreamConnectors#extractRuntimeStreams",
    "extract_telemetry_runtime": "io.webweavex.connectors.TelemetryConnector#extractTelemetryRuntime",
    # Session 4B — pure document + pagination extraction (dependency-proof survivors)
    "extract_document_runtime": "io.webweavex.documents.DocumentRuntime#extractDocumentRuntime",
    "extract_paginated_content": "io.webweavex.interaction.Pagination#extractPaginatedContent",
    # Session 6 — interaction graph (dependency-clean)
    "build_interaction_graph": "io.webweavex.interaction.InteractionGraph#buildInteractionGraph",
    # Session 7 — remaining connector-runtime cluster (dependency-clean)
    "extract_container_runtime": "io.webweavex.connectors.ContainerConnector#extractContainerRuntime",
    "extract_ide_runtime": "io.webweavex.connectors.IdeConnector#extractIdeRuntime",
    "extract_kubernetes_runtime": "io.webweavex.connectors.KubernetesConnector#extractKubernetesRuntime",
    # Session 8 — session-crypto cluster + json.loads substrate (PyJsonParse)
    "encrypt_session_state": "io.webweavex.crypto.KaalkaSession#encryptSessionState",
    "decrypt_session_state": "io.webweavex.crypto.KaalkaSession#decryptSessionState",
    "save_encrypted_session": "io.webweavex.session.EncryptedSessionStore#saveEncryptedSession",
    "load_encrypted_session": "io.webweavex.session.EncryptedSessionStore#loadEncryptedSession",
    # Session 9 — execution family (dependency-clean, 26-module closure)
    "build_runtime_sandbox": "io.webweavex.execution.ExecutionRuntime#buildRuntimeSandbox",
    "execute_runtime_action": "io.webweavex.execution.ExecutionRuntime#executeRuntimeAction",
    "replay_runtime_execution": "io.webweavex.execution.ExecutionRuntime#replayRuntimeExecution",
    "simulate_runtime_execution": "io.webweavex.execution.ExecutionRuntime#simulateRuntimeExecution",
    "run_execution_runtime": "io.webweavex.execution.ExecutionRuntime#runExecutionRuntime",
    "run_execution_for_extraction": "io.webweavex.execution.ExecutionRuntime#runExecutionForExtraction",
    # Session 10 — synchronization family (dependency-clean, 25-module closure)
    "build_runtime_delta": "io.webweavex.synchronization.SyncRuntime#buildRuntimeDelta",
    "replay_synchronized_runtime": "io.webweavex.synchronization.SyncRuntime#replaySynchronizedRuntime",
    "run_synchronized_runtime": "io.webweavex.synchronization.SyncRuntime#runSynchronizedRuntime",
    "run_sync_for_extraction": "io.webweavex.synchronization.SyncRuntime#runSyncForExtraction",
    "save_sync_memory": "io.webweavex.synchronization.SyncRuntime#saveSyncMemory",
    "load_sync_memory": "io.webweavex.synchronization.SyncRuntime#loadSyncMemory",
    # Session 11 — workflows family (dependency-clean, 23-module closure)
    "build_runtime_objective": "io.webweavex.workflow.WorkflowRuntime#buildRuntimeObjective",
    "build_workflow_plan": "io.webweavex.workflow.WorkflowRuntime#buildWorkflowPlan",
    "run_autonomous_workflow": "io.webweavex.workflow.WorkflowRuntime#runAutonomousWorkflow",
    "replay_workflow_runtime": "io.webweavex.workflow.WorkflowRuntime#replayWorkflowRuntime",
    "run_workflow_for_extraction": "io.webweavex.workflow.WorkflowRuntime#runWorkflowForExtraction",
    "save_workflow_memory": "io.webweavex.workflow.WorkflowRuntime#saveWorkflowMemory",
    "load_workflow_memory": "io.webweavex.workflow.WorkflowRuntime#loadWorkflowMemory",
    # Session 12 — evolution_runtime family (dependency-clean, 25-module closure)
    "build_runtime_evolution": "io.webweavex.evolution.EvolutionRuntime#buildRuntimeEvolution",
    "evolve_selector_runtime": "io.webweavex.evolution.EvolutionRuntime#evolveSelectorRuntime",
    "run_evolution_runtime": "io.webweavex.evolution.EvolutionRuntime#runEvolutionRuntime",
    "run_evolution_for_extraction": "io.webweavex.evolution.EvolutionRuntime#runEvolutionForExtraction",
    "save_evolution_runtime": "io.webweavex.evolution.EvolutionRuntime#saveEvolutionRuntime",
    "load_evolution_runtime": "io.webweavex.evolution.EvolutionRuntime#loadEvolutionRuntime",
    # Session 13 — causality family (dependency-clean, 25-module closure)
    "run_causality_runtime": "io.webweavex.causality.CausalityRuntime#runCausalityRuntime",
    "replay_causal_runtime": "io.webweavex.causality.CausalityRuntime#replayCausalRuntime",
    "run_causality_for_extraction": "io.webweavex.causality.CausalityRuntime#runCausalityForExtraction",
    "save_causal_memory": "io.webweavex.causality.CausalityRuntime#saveCausalMemory",
    "load_causal_memory": "io.webweavex.causality.CausalityRuntime#loadCausalMemory",
    # Session 14 — streaming + live_runtime family (dependency-clean)
    "build_stream_timeline": "io.webweavex.streaming.StreamingRuntime#buildStreamTimeline",
    "replay_stream_events": "io.webweavex.streaming.StreamingRuntime#replayStreamEvents",
    "run_live_runtime": "io.webweavex.streaming.StreamingRuntime#runLiveRuntime",
    "save_live_runtime": "io.webweavex.streaming.StreamingRuntime#saveLiveRuntime",
    "load_live_runtime": "io.webweavex.streaming.StreamingRuntime#loadLiveRuntime",
    # Session 15 — adaptive modal recovery (dependency-clean, 1 module)
    "recover_modal_runtime": "io.webweavex.adaptive.ModalRecovery#recoverModalRuntime",
    # Session 16 — reconstruction orchestrator (dependency-clean, 24-module closure)
    "run_reconstruction_runtime": "io.webweavex.reconstruction.ReconstructionRuntime#runReconstructionRuntime",
    "run_reconstruction_for_extraction": "io.webweavex.reconstruction.ReconstructionRuntime#runReconstructionForExtraction",
    # Session 17 — memory persistence x4 (dependency-clean; runtime/semantic/adaptive/application)
    "save_runtime_memory": "io.webweavex.memory.MemoryPersistence#saveRuntimeMemory",
    "load_runtime_memory": "io.webweavex.memory.MemoryPersistence#loadRuntimeMemory",
    "save_semantic_memory": "io.webweavex.memory.MemoryPersistence#saveSemanticMemory",
    "load_semantic_memory": "io.webweavex.memory.MemoryPersistence#loadSemanticMemory",
    "save_adaptive_memory": "io.webweavex.memory.MemoryPersistence#saveAdaptiveMemory",
    "load_adaptive_memory": "io.webweavex.memory.MemoryPersistence#loadAdaptiveMemory",
    "save_application_memory": "io.webweavex.memory.MemoryPersistence#saveApplicationMemory",
    "load_application_memory": "io.webweavex.memory.MemoryPersistence#loadApplicationMemory",
    # Session 18 — browser identity (dependency-clean, 28-module closure)
    "build_browser_identity": "io.webweavex.identity.IdentityRuntime#buildBrowserIdentity",
    "save_browser_identity": "io.webweavex.identity.IdentityRuntime#saveBrowserIdentity",
    "load_browser_identity": "io.webweavex.identity.IdentityRuntime#loadBrowserIdentity",
    # Session 19 — clean remainder slice (persistence + pure transforms + S16 freebies)
    "save_distributed_checkpoint": "io.webweavex.distributed.DistributedCheckpoint#saveDistributedCheckpoint",
    "load_distributed_checkpoint": "io.webweavex.distributed.DistributedCheckpoint#loadDistributedCheckpoint",
    "save_native_runtime": "io.webweavex.memory.NativeRuntimePersistence#saveNativeRuntime",
    "load_native_runtime": "io.webweavex.memory.NativeRuntimePersistence#loadNativeRuntime",
    "replay_semantic_runtime": "io.webweavex.semantic.SemanticReplay#replaySemanticRuntime",
    "execute_runtime_objective": "io.webweavex.application.ObjectiveExecution#executeRuntimeObjective",
    "query_repository": "io.webweavex.repository.RepositoryQuery#queryRepository",
    "authenticate_runtime": "io.webweavex.auth.AuthenticationRuntime#authenticateRuntime",
    "clone_runtime_environment": "io.webweavex.reconstruction.ReconstructionRuntime#cloneRuntimeEnvironment",
    "fabricate_runtime_reality": "io.webweavex.reconstruction.ReconstructionRuntime#fabricateRuntimeReality",
    # Session 20 — memory orchestrator (final clean slice, 37-module closure)
    "run_runtime_memory": "io.webweavex.memory.RuntimeMemoryRuntime#runRuntimeMemory",
    "run_memory_for_extraction": "io.webweavex.memory.RuntimeMemoryRuntime#runMemoryForExtraction",
    # Session 21 — Tier-B start: heal_selector portable (empty-HTML) contract
    "heal_selector": "io.webweavex.adaptive.SelectorHealing#healSelector",
}

PACKAGES = [
    "adaptive", "agents", "application", "auth", "browser", "causality", "connectors", "crypto", "crawling",
    "determinism", "distributed", "documents", "evolution", "execution",
    "extraction", "graph", "identity", "ingestion", "interaction", "ir",
    "kernel", "layout", "memory", "multimodal", "ocr", "orchestration",
    "parity", "persistence", "query", "reasoning", "reconstruction", "replay",
    "repository", "runtime", "semantic", "session", "streaming", "synchronization",
    "tables", "vision", "workflow",
]


def java_status(api: str) -> str:
    if api in JAVA_PROVEN:
        return "✅ Implemented (parity-proven)"
    return "⬜ Planned"


def yn(flag: bool) -> str:
    return "✓" if flag else "—"


def main() -> None:
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    apis = sorted(manifest["apis"], key=lambda a: a["api"].lower())
    proven = sum(1 for a in apis if a["api"] in JAVA_PROVEN)

    lines = []
    lines.append("# JAVA_PARITY_MATRIX")
    lines.append("")
    lines.append(
        "Generated by `tools/gen_java_parity_matrix.py` from "
        "`PARITY_MANIFEST.json` — the single source of truth shared by the "
        "Python (canonical), JavaScript, and Dart runtimes. Do not edit by hand."
    )
    lines.append("")
    lines.append("## Goal")
    lines.append("")
    lines.append("`Python = Java = JavaScript = Dart` — identical public APIs, "
                 "deterministic outputs, canonical JSON, Kaalka hashes, and "
                 "replay/reconstruction behavior. The Java port is built "
                 "**foundation-first**: the deterministic + cryptographic bedrock "
                 "is implemented and byte-exact-verified before any higher layer, "
                 "because every other subsystem hashes/serializes through it.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    c = manifest["counts"]
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Total tracked public APIs | {len(apis)} |")
    lines.append(f"| Python / JS / Dart Complete | {c['Complete']} |")
    lines.append(f"| Python / JS / Dart Partial | {c['Partial']} |")
    lines.append(f"| Python / JS / Dart Deferred | {c['Deferred']} |")
    lines.append(f"| **Java implemented (parity-proven)** | **{proven}** |")
    lines.append(f"| **Java planned** | **{len(apis) - proven}** |")
    lines.append("")
    lines.append("> Parity is proven transitively: Python ≡ JavaScript ≡ Dart is "
                 "already certified (70k+ byte-identical comparisons, see repo "
                 "certification reports). This slice proves **Java ≡ Python** for "
                 "the foundation primitives with 80 byte-exact assertions "
                 "(`CrossLanguageParityTest`), which therefore proves Java ≡ JS ≡ "
                 "Dart for those primitives.")
    lines.append("")
    lines.append("## Target package structure (`io.webweavex.*`)")
    lines.append("")
    lines.append("Mirrors the Python `core/`, JavaScript `src/`, and Dart "
                 "`lib/src/` layouts:")
    lines.append("")
    implemented_pkgs = ("determinism", "crypto", "graph", "ir", "kernel",
                        "persistence", "replay", "query", "memory", "reconstruction",
                        "connectors", "documents", "execution", "interaction", "session",
                        "synchronization", "workflow", "evolution", "causality", "streaming", "adaptive", "identity",
                        "distributed", "semantic", "application", "repository", "auth")
    for pkg in PACKAGES:
        mark = " — **implemented**" if pkg in implemented_pkgs else (
            " — **test harness**" if pkg == "parity" else "")
        lines.append(f"- `io.webweavex.{pkg}`{mark}")
    lines.append("")
    lines.append("## API parity table")
    lines.append("")
    lines.append("| API | Python | JS | Dart | P/JS/Dart class | Java status |")
    lines.append("| --- | :---: | :---: | :---: | :---: | --- |")
    for a in apis:
        lines.append(
            f"| `{a['api']}` | {yn(a.get('python'))} | {yn(a.get('javascript'))} "
            f"| {yn(a.get('dart'))} | {a['classification']} | {java_status(a['api'])} |"
        )
    lines.append("")
    lines.append("## Implemented foundation primitives (internal, parity-proven)")
    lines.append("")
    lines.append("These underpin every public API and are byte-exact to Python/Dart:")
    lines.append("")
    lines.append("- `io.webweavex.determinism.Normalization` — NFKC + CRLF + "
                 "trailing-whitespace strip, code-point key ordering, "
                 "volatile-key stripping, numeric canonicalization")
    lines.append("- `io.webweavex.determinism.PyFloat` — Python `repr(float)` "
                 "(shortest round-trip, positional/scientific thresholds)")
    lines.append("- `io.webweavex.determinism.CanonicalJson` — compact, "
                 "sorted-key, `ensure_ascii=False` JSON encoder")
    lines.append("- `io.webweavex.determinism.StableSerialize` — canonical "
                 "string form used for hashing/encryption")
    lines.append("- `io.webweavex.crypto.Hashing` — `sha256(utf8(stableSerialize))`")
    lines.append("- `io.webweavex.crypto.KaalkaV5Proc` / `TimeKey` / `Kaalka` — "
                 "Kaalka v5 cipher, time-key derivation, encrypt/decrypt/hash")
    lines.append("")
    lines.append("## Next sessions (planned order, dependency-driven)")
    lines.append("")
    for i, step in enumerate([
        "kernel + ir + graph (RuntimeKernel, UniversalInput, RuntimeGraph, runtime IR)",
        "fingerprint + replay + reconstruction (compute_global_runtime_fingerprint, replay equivalence)",
        "query engines (graph/document/repository/knowledge/semantic IR)",
        "memory + persistence + synchronization",
        "extraction (HTML/document/repository) + universal_extract",
        "semantic + evidence + workflow + evolution",
        "vision + ocr + multimodal (no placeholders)",
        "release engineering (javadoc, GPG, Sonatype, CI, certification reports)",
    ], 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print(f"wrote {OUT} ({len(apis)} APIs, {proven} Java-proven)")


if __name__ == "__main__":
    main()
