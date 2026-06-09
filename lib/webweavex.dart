/// WebWeaveX — deterministic runtime cognition infrastructure (Dart).
library;

export 'src/browser/authenticated_runtime.dart';
export 'src/browser/browser_identity.dart';
export 'src/browser/capture_runtime.dart';
export 'src/browser/extract_web.dart';
export 'src/browser/render_page.dart';
export 'src/browser/runtime_continuation.dart';
export 'src/browser/runtime_session.dart';
export 'src/browser/runtime_snapshot.dart';
export 'src/browser/spa_stabilizer.dart';
export 'src/crypto/kaalka_runtime.dart';
export 'src/determinism/dom_stabilization.dart';
export 'src/determinism/fingerprint.dart';
export 'src/determinism/normalization.dart';
export 'src/determinism/stable_serialize.dart';
export 'src/graph/runtime_graph.dart';
export 'src/graph/runtime_graph_reconstruction.dart';
export 'src/graph/runtime_graph_replay.dart';
export 'src/kernel/reconstruction_pipeline.dart';
export 'src/kernel/replay_pipeline.dart';
export 'src/kernel/runtime_pipeline.dart';
export 'src/memory/memory_lineage.dart';
export 'src/memory/memory_replay.dart';
export 'src/memory/query_memory.dart';
export 'src/memory/runtime_memory.dart';
export 'src/memory/runtime_memory_graph.dart';
export 'src/reconstruction/reconstruct_browser.dart';
export 'src/reconstruction/reconstruct_graph.dart';
export 'src/reconstruction/reconstruct_memory.dart';
export 'src/reconstruction/reconstruct_replay.dart';
export 'src/reconstruction/reconstruct_runtime.dart';
export 'src/replay/replay_dom.dart';
export 'src/replay/replay_equivalence.dart';
export 'src/replay/replay_fingerprint.dart';
export 'src/replay/replay_graph.dart';
export 'src/replay/replay_memory.dart';
export 'src/replay/replay_runtime.dart';
export 'src/connectors/connectors_impl.dart';
export 'src/connectors/postgres_connector.dart';
export 'src/distributed/distributed_extraction_orchestrator.dart';
export 'src/orchestration/orchestration_engine.dart';
export 'src/semantic/semantic_memory.dart';

// Runtime-cognition families ported with proven cross-language hash parity
// (see test/parity/ and validation/parity/*_api_vectors.json). Exported by
// explicit name to keep the public surface = the Python __all__ parity set.
export 'src/causality/causality.dart'
    show
        runCausalityRuntime,
        runCausalityForExtraction,
        saveCausalMemory,
        loadCausalMemory,
        replayCausalRuntime;
export 'src/semantic/semantic_runtime.dart'
    show
        runSemanticRuntime,
        runSemanticForExtraction,
        saveSemanticMemory,
        loadSemanticMemory,
        replaySemanticRuntime;
export 'src/synchronization/synchronization.dart'
    show
        runSynchronizedRuntime,
        runSyncForExtraction,
        buildRuntimeDelta,
        saveSyncMemory,
        loadSyncMemory,
        replaySynchronizedRuntime;
export 'src/evolution/evolution_runtime.dart'
    show
        runEvolutionRuntime,
        runEvolutionForExtraction,
        buildRuntimeEvolution,
        evolveSelectorRuntime,
        saveEvolutionRuntime,
        loadEvolutionRuntime;
export 'src/workflows/workflows.dart'
    show
        runAutonomousWorkflow,
        runWorkflowForExtraction,
        buildRuntimeObjective,
        buildWorkflowPlan,
        saveWorkflowMemory,
        loadWorkflowMemory,
        replayWorkflowRuntime;
export 'src/execution/execution.dart'
    show
        runExecutionRuntime,
        runExecutionForExtraction,
        executeRuntimeAction,
        buildRuntimeSandbox,
        simulateRuntimeExecution,
        replayRuntimeExecution;

const version = '2.0.0';
