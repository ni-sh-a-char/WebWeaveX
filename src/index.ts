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

export { buildUnifiedRuntimeIR, compileRuntimeIR } from "./ir/unifiedIr.js";
export {
  buildRuntimeGraph,
  queryRuntimeGraph,
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

export type { UniversalInput, PipelineOptions, ExtractionEnvelope } from "./contracts/runtimeContracts.js";
export type { RuntimeGraph } from "./contracts/graphContracts.js";

export const VERSION = "2.0.0";
