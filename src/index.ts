export { extractWeb } from "./browser/extractWeb.js";
export { renderPage } from "./browser/renderPage.js";
export { captureRuntime, captureDom } from "./browser/captureRuntime.js";
export {
  saveAuthenticatedRuntime,
  loadAuthenticatedRuntime,
  rotateAuthenticatedSession,
} from "./browser/authenticatedRuntime.js";

export { runCanonicalPipeline } from "./kernel/runtimePipeline.js";

export { computeGlobalRuntimeFingerprint } from "./determinism/globalRuntimeFingerprint.js";
export { computeStableDomHash, computeSpaFingerprint, stabilizeDomHtml } from "./determinism/domStabilization.js";
export { normalizeRuntimeState, normalizeRuntimeGraph } from "./determinism/normalizeRuntime.js";

export { validateReplayEquivalence } from "./replay/replayEquivalence.js";

export {
  reconstructRuntime,
  replayRuntime,
  rebuildExecutionGraph,
} from "./reconstruction/reconstructRuntime.js";

export {
  buildRuntimeMemory,
  mergeRuntimeMemories,
  queryRuntimeMemory,
  replicateRuntimeMemory,
  stableMemoryHash,
} from "./memory/runtimeMemory.js";

export { runExecutionRuntime } from "./execution/executionRuntime.js";

export { buildUnifiedRuntimeIR, compileRuntimeIR } from "./ir/unifiedIr.js";
export { buildRuntimeGraph, queryRuntimeGraph, graphFingerprint } from "./graph/runtimeGraph.js";

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
