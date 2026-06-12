/**
 * RULE 15 — public API equality. The JavaScript package must expose a
 * specification-equivalent name for every public name in the Python
 * `webweavex` package __all__ (snake_case → camelCase). The authoritative
 * name list is committed alongside this test and regenerated from the
 * specification surface.
 */
import { describe, expect, it } from "vitest";
import * as webweavex from "../../src/index.js";

// camelCase counterparts of origin/python:webweavex/__init__.py __all__ (128).
const REQUIRED_PUBLIC_API = [
  "RuntimeKernel", "UniversalInput", "VERSION", "version", "analyze",
  "authenticateRuntime", "buildBrowserIdentity", "buildInteractionGraph",
  "buildRuntimeDelta", "buildRuntimeEvolution", "buildRuntimeGraph",
  "buildRuntimeMemory", "buildRuntimeObjective", "buildRuntimeSandbox",
  "buildStreamTimeline", "buildWorkflowPlan", "captureDomMutations",
  "captureWebsocketFrames", "cloneRuntimeEnvironment", "compileDocument",
  "compileRepository", "compileUnifiedRuntimeIr", "computeGlobalRuntimeFingerprint",
  "computeKaalkaHash", "crawl", "crawlAsync", "decryptSessionState", "decryptValue",
  "encryptSessionState", "encryptValue", "evolveSelectorRuntime", "executeRuntimeAction",
  "executeRuntimeObjective", "extract", "extractApiRuntime", "extractAsync",
  "extractContainerRuntime", "extractDatabaseRuntime", "extractDocs",
  "extractDocumentRuntime", "extractIdeRuntime", "extractInfiniteScroll",
  "extractKubernetesRuntime", "extractMultimodal", "extractNative",
  "extractPaginatedContent", "extractRecursive", "extractRepo", "extractRepository",
  "extractRuntimeStreams", "extractTelemetryRuntime", "extractWeb",
  "fabricateRuntimeReality", "fingerprint", "getRuntimeKernel", "healSelector",
  "ingestInput", "loadAdaptiveMemory", "loadApplicationMemory", "loadBrowserIdentity",
  "loadCausalMemory", "loadDistributedCheckpoint", "loadEncryptedSession",
  "loadEvolutionRuntime", "loadLiveRuntime", "loadNativeRuntime", "loadRuntimeMemory",
  "loadSemanticMemory", "loadSyncMemory", "loadWorkflowMemory", "queryDocuments",
  "queryGraph", "queryKnowledge", "queryRepo", "queryRepository", "queryRuntimeGraph",
  "queryRuntimeMemory", "querySemantics", "reasonSemantically", "reconstructRuntime",
  "recoverModalRuntime", "replayCausalRuntime", "replayInteractions",
  "replayRuntimeExecution", "replaySemanticRuntime", "replayStreamEvents",
  "replaySynchronizedRuntime", "replayWorkflowRuntime", "runApplicationCognition",
  "runAutonomousExtraction", "runAutonomousWorkflow", "runCanonicalPipeline",
  "runCausalityForExtraction", "runCausalityRuntime", "runEvolutionForExtraction",
  "runEvolutionRuntime", "runExecutionForExtraction", "runExecutionRuntime",
  "runLiveRuntime", "runMemoryForExtraction", "runNativeCognition",
  "runReconstructionForExtraction", "runReconstructionRuntime", "runRuntimeMemory",
  "runSemanticForExtraction", "runSemanticRuntime", "runSyncForExtraction",
  "runSynchronizedRuntime", "runWorkflowForExtraction", "saveAdaptiveMemory",
  "saveApplicationMemory", "saveBrowserIdentity", "saveCausalMemory",
  "saveDistributedCheckpoint", "saveEncryptedSession", "saveEvolutionRuntime",
  "saveLiveRuntime", "saveNativeRuntime", "saveRuntimeMemory", "saveSemanticMemory",
  "saveSyncMemory", "saveWorkflowMemory", "searchRuntimeMemory",
  "simulateRuntimeExecution", "streamExtract", "universalExtract",
  "validateReconstructedRuntime", "validateReplayEquivalence",
] as const;

describe("RULE 15 — public API equality (Python __all__ ⇄ JS exports)", () => {
  const surface = webweavex as Record<string, unknown>;

  it("exposes every Python public API name", () => {
    const missing = REQUIRED_PUBLIC_API.filter((n) => !(n in surface));
    expect(missing).toEqual([]);
  });

  it("exposes each name as a callable function (or the version string)", () => {
    const wrongType = REQUIRED_PUBLIC_API.filter((n) => {
      const v = surface[n];
      if (n === "VERSION" || n === "version") return typeof v !== "string";
      if (n === "RuntimeKernel" || n === "UniversalInput") return typeof v !== "function";
      return typeof v !== "function";
    });
    expect(wrongType).toEqual([]);
  });

  it("convenience wrappers return bounded specification-shaped results", () => {
    const a = (webweavex.analyze as (i: unknown, e?: unknown) => Record<string, unknown>)([{ id: "n1" }], []);
    expect(typeof a).toBe("object");
    const cd = (webweavex.compileDocument as (t: string) => Record<string, unknown>)("hello world");
    expect(cd && typeof cd).toBe("object");
    expect((webweavex.version as string)).toBe("2.1.0");
  });
});
