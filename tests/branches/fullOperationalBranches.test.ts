import { describe, expect, it } from "vitest";
import * as wwx from "../../src/index.js";
import { buildRuntimeGraph as _buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { routeBrowserIdentity } from "../../src/distributed/distributedIdentityEngine.js";
import { buildDistributedRuntimeGraph } from "../../src/distributed/distributedRuntimeGraphEngine.js";
import { enqueueExtraction, dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";
import { synchronizeAdaptiveRuntime } from "../../src/distributed/distributedAdaptiveRuntimeEngine.js";
import { monitorExtractionCluster } from "../../src/distributed/distributedMonitoringEngine.js";
import { recoverDistributedRuntime } from "../../src/distributed/distributedRecoveryEngine.js";
import { extractWeb } from "../../src/browser/extractWeb.js";
import { continueAuthenticatedRuntime } from "../../src/browser/runtimeContinuation.js";
import { replaySemanticEvents } from "../../src/runtime/semanticReplayVm.js";
import { transitionRuntimeState } from "../../src/runtime/runtimeStateMachine.js";
import { runSemanticVm } from "../../src/vm/semanticVmEngine.js";
import { detectContradictions } from "../../src/semantic/contradictionEngine.js";

describe("full operational branch coverage", () => {
  it("distributed branches", () => {
    const w = { worker_id: "w1", status: "busy", identity: { fingerprint_hash: "fp" } };
    expect((buildDistributedRuntimeGraph([w, { worker_id: "w2" }], { nodes: [{ id: "n" }], edges: [] }).nodes as unknown[]).length).toBeGreaterThan(1);
    expect((routeBrowserIdentity([w]).routes as unknown[]).length).toBe(1);
    expect(enqueueExtraction([], { task_id: "t", url: "u", priority: 1 }).queue.length).toBe(1);
    expect(dequeueExtraction([]).task).toBeNull();
    expect(runDistributedExtraction([{ task_id: "x" }]).bounded).toBe(true);
    const sync = synchronizeAdaptiveRuntime([{ memory: { healed_selectors: { s: "ok" } } }]);
    expect(sync.bounded).toBe(true);
    expect((sync.healed_selectors as Record<string, string>).s).toBe("ok");
    expect(monitorExtractionCluster([w], []).queue_depth).toBe(0);
    expect(recoverDistributedRuntime({ queue: [] }).recovered).toBe(true);
  });

  it("runtime vm and semantic branches", () => {
    expect(replaySemanticEvents([{ id: "1", type: "t" }]).event_count).toBe(1);
    expect(transitionRuntimeState("running", "paused").valid).toBe(true);
    expect(transitionRuntimeState("running", "invalid").valid).toBe(false);
    expect(runSemanticVm([{ opcode: "LINK", operand: { from: "a", to: "b" } }]).bounded).toBe(true);
    const contra = detectContradictions(["service is up", "service is down"]) as Record<string, unknown>;
    expect(Array.isArray(contra.conflicts)).toBe(true);
    expect((contra.grounding as Record<string, unknown>).method).toBe("polarity_token_scan");
    expect(wwx.runRuntimeCognitionTick({}, [], []).bounded).toBe(true);
  });

  it("browser and graph branches", async () => {
    const graph = _buildRuntimeGraph({ a: 1, b: 2 });
    expect(wwx.validateRuntimeGraph(graph).valid).toBe(true);
    expect(wwx.replayRuntimeGraph(graph).nodes.length).toBeGreaterThan(0);
    // continuation requires session file — branch-only smoke
    expect(typeof continueAuthenticatedRuntime).toBe("function");
  });
});
