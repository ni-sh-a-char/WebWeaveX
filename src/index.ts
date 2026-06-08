export { extractWeb } from "./browser/extractWeb.js";
export { renderPage } from "./browser/renderPage.js";
export { captureRuntime, captureDom } from "./browser/captureRuntime.js";
export {
  saveAuthenticatedRuntime,
  loadAuthenticatedRuntime,
  rotateAuthenticatedSession,
} from "./browser/authenticatedRuntime.js";
export {
  createRuntimeSession,
  persistRuntimeSession,
  restoreRuntimeSession,
  rotateRuntimeSession,
} from "./browser/runtimeSession.js";
export { captureRuntimeSnapshot, compareRuntimeSnapshots } from "./browser/runtimeSnapshot.js";
export { buildBrowserIdentity, identityFromExtraction, compareBrowserIdentity } from "./browser/browserIdentity.js";
export { detectSpaFramework, stabilizeSpaDom } from "./browser/spaStabilizer.js";
export { continueAuthenticatedRuntime, extractWithSession } from "./browser/runtimeContinuation.js";

export * from "./connectors/index.js";
export { runDistributedExtraction } from "./distributed/distributedExtractionOrchestrator.js";
export { orchestrate } from "./orchestration/orchestrationEngine.js";
export { runAutonomousWorkflow, replayWorkflowRuntime } from "./workflows/workflowOrchestrator.js";
export { SemanticMemory, buildSemanticMemory } from "./semantic/semanticMemory.js";
export { runSemanticRuntime } from "./semantic/semanticRuntime.js";
export { replayDomSnapshot, validateDomReplayEquivalence } from "./replay/replayDom.js";
export { buildRuntimeGraphLineage } from "./graph/runtimeGraphLineage.js";

export { runCanonicalPipeline } from "./kernel/runtimePipeline.js";

export { computeGlobalRuntimeFingerprint } from "./determinism/globalRuntimeFingerprint.js";
export { computeStableDomHash, computeSpaFingerprint, stabilizeDomHtml } from "./determinism/domStabilization.js";
export { normalizeRuntimeState, normalizeRuntimeGraph } from "./determinism/normalizeRuntime.js";

export { validateReplayEquivalence } from "./replay/replayEquivalence.js";
export { replayRuntimeState, validateFullRuntimeReplay } from "./replay/replayRuntime.js";
export { replayRuntimeGraph, validateGraphReplayEquivalence, graphReplayHash } from "./replay/replayGraph.js";
export { replayRuntimeMemory, validateMemoryReplayEquivalence, memoryReplayHash } from "./replay/replayMemory.js";
export {
  computeReplayFingerprint,
  validateFingerprintReplayEquivalence,
} from "./replay/replayFingerprint.js";

export {
  reconstructRuntime,
  replayRuntime,
  rebuildExecutionGraph,
  reconstructReplayState,
  reconstructRuntimeGraph,
  reconstructMemoryFromEnvelope,
  reconstructBrowserState,
} from "./reconstruction/reconstructRuntime.js";

export {
  buildRuntimeMemory,
  mergeRuntimeMemories,
  queryRuntimeMemory,
  replicateRuntimeMemory,
  stableMemoryHash,
} from "./memory/runtimeMemory.js";
export { buildRuntimeMemoryGraph } from "./memory/runtimeMemoryGraph.js";
export { buildMemoryLineage, verifyMemoryLineage } from "./memory/memoryLineage.js";
export { saveRuntimeMemory, loadRuntimeMemory } from "./memory/memoryPersistence.js";
export { replayMemoryState, validateMemoryReplay } from "./memory/memoryReplay.js";

export { runExecutionRuntime } from "./execution/executionRuntime.js";
export { recoverRuntime } from "./runtime/runtimeRecoveryEngine.js";
export { replaySemanticEvents } from "./runtime/semanticReplayVm.js";
export { runRuntimeCognitionTick } from "./cognition/runtimeCognitionEngine.js";
export { createSemanticJournal } from "./semantic/semanticJournal.js";
export { createSemanticSnapshot, restoreSemanticSnapshot } from "./semantic/semanticSnapshot.js";
export { makeStreamEvent } from "./streaming/streamCapture.js";
export { saveStreamRuntime, loadStreamRuntime, mergeStreamRuntimes } from "./streaming/streamPersistence.js";
export { detectBuildSystems } from "./repository/buildSystemDetection.js";
export { inferFromEvidence } from "./evidence/semanticInferenceCalculus.js";
export { extractCitations } from "./documents/documentExtraction.js";

export { buildUnifiedRuntimeIR, compileRuntimeIR } from "./ir/unifiedIr.js";
// buildRuntimeGraph / queryRuntimeGraph are the SPEC public API names
// (core.runtime_graph, list-of-IRs / (graph, query)). They are provided by
// publicApi.ts from the certified src/runtime_graph ports. The dict-based
// helpers in ./graph/runtimeGraph.js are JS-internal (imported directly by
// the pipeline) and intentionally NOT the public exports.
export {
  graphFingerprint,
  computeRuntimeFingerprint,
  validateRuntimeGraph,
} from "./graph/runtimeGraph.js";
export { replayGraphLineage, mergeGraphReplay } from "./graph/runtimeGraphReplay.js";
export { reconstructGraphFromIr, rebuildGraphFromPartial } from "./graph/runtimeGraphReconstruction.js";
export { computeGraphLineageFingerprint } from "./graph/runtimeGraphFingerprint.js";

export {
  encryptValue,
  decryptValue,
  deriveKaalkaTimeKey,
  normalizeRuntimeValue,
  stableSerialize,
  computeDeterministicHash,
  computeDeterministicHashPayload,
  computeKaalkaHash,
  computeKaalkaHashPayload,
  KAALKA_ALGORITHM,
  KAALKA_NPM_VERSION,
} from "./crypto/kaalkaRuntime.js";
export { VOLATILE_RUNTIME_KEYS } from "./determinism/normalization.js";

// UniversalInput is a class (runtime value + type) in the spec public API
export { UniversalInput } from "./contracts/runtimeContracts.js";
export type { PipelineOptions, ExtractionEnvelope } from "./contracts/runtimeContracts.js";
export type { RuntimeGraph } from "./contracts/graphContracts.js";

export const VERSION = "2.0.1";

// Specification-conforming public API surface (mirrors the Python `webweavex`
// package __all__). Generated by tools/convergence/build_public_api.py.
export * from "./publicApi.js";
