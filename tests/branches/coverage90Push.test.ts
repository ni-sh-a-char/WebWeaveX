import { describe, expect, it } from "vitest";
import { mkdtempSync, writeFileSync, rmSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { runAdaptiveExtraction } from "../../src/adaptive/adaptiveOrchestrator.js";
import { healSelector, computeDomSimilarity } from "../../src/adaptive/selectorHealing.js";
import { runLiveRuntime } from "../../src/connectors/liveRuntimeOrchestrator.js";
import { extractContainerRuntime } from "../../src/connectors/containerConnector.js";
import { runRuntimeCognitionTick } from "../../src/cognition/runtimeCognitionEngine.js";
import { runOntologyRuntime } from "../../src/semantic/ontologyRuntime.js";
import { reconcileSemanticStates } from "../../src/semantic/semanticReconciliation.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { replaySemanticEvents } from "../../src/runtime/semanticReplayVm.js";
import { recoverDistributedRuntime } from "../../src/distributed/distributedRecoveryEngine.js";
import { balanceExtractionWorkloads } from "../../src/distributed/distributedLoadBalancer.js";
import { buildDistributedRuntimeGraph } from "../../src/distributed/distributedRuntimeGraphEngine.js";
import { federateStreamRuntimes } from "../../src/distributed/distributedStreamEngine.js";
import { buildClusterState } from "../../src/distributed/distributedClusterEngine.js";
import { enqueueExtraction, dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";
import { createExtractionWorker } from "../../src/distributed/extractionWorkerEngine.js";
import { validateInference } from "../../src/evidence/inferenceValidation.js";
import { loadRuntimeMemory, saveRuntimeMemory } from "../../src/memory/memoryPersistence.js";
import { registerParser, getParser, listParsers } from "../../src/parsers/parserRegistry.js";
import { runSemanticVm, SemanticVirtualMachine } from "../../src/vm/semanticVmEngine.js";
import { cognizeRuntimeEnvironment } from "../../src/worldModel/runtimeEnvironmentCognition.js";
import { buildSemanticWorldGraph } from "../../src/worldModel/semanticWorldGraph.js";
import { compileWorldModel } from "../../src/worldModel/worldModelCompile.js";
import { modelOperationalTopology } from "../../src/worldModel/operationalTopologyModel.js";
import { extractWithSession } from "../../src/browser/runtimeContinuation.js";
import { createRuntimeSession } from "../../src/browser/runtimeSession.js";

describe("coverage 90% branch push", () => {
  it("adaptive orchestrator all selector branches", () => {
    expect(runAdaptiveExtraction("#hello", "  a  b  ", [{ text: "hello" }]).healed_selector).toBe("#hello");
    expect(runAdaptiveExtraction("#miss", "x", [{ attrs: { id: "node1" } }]).healed_selector).toBe("#node1");
    expect(runAdaptiveExtraction("#miss", "x", [{ attrs: {} }]).healed_selector).toBe("#root");
    expect(runAdaptiveExtraction("#only", "x", []).healed_selector).toBe("#only");
    const healed = healSelector("#t", [
      { attrs: { id: "a", "data-testid": "btn" }, text: "target" },
      { text: "other" },
    ]);
    expect((healed.strategies as unknown[]).length).toBeGreaterThan(1);
    expect(computeDomSimilarity("a b", "a b c")).toBeGreaterThan(0);
    expect(computeDomSimilarity("", "x")).toBe(0);
    expect(computeDomSimilarity("same", "same")).toBe(1);
  });

  it("distributed engines optional branches", () => {
    expect(recoverDistributedRuntime({ state: { tick: 3 } }).recovered).toBe(true);
    expect((recoverDistributedRuntime({ state: { tick: 3 } }).state as Record<string, unknown>).tick).toBe(3);
    expect(recoverDistributedRuntime({}).state).toEqual({});
    expect(balanceExtractionWorkloads([], [{ task_id: "t" }]).assignments).toEqual([]);
    expect(
      (balanceExtractionWorkloads([{ worker_id: "w" }], [{}, { task_id: "explicit" }]).assignments as unknown[]).length,
    ).toBe(2);
    expect(
      (buildDistributedRuntimeGraph(
        [{ status: "busy" }, { worker_id: "w2" }],
        { nodes: [{ id: "n1", type: "federation" }] },
      ).edges as unknown[]).length,
    ).toBe(1);
    expect(federateStreamRuntimes([{ events: [1, 2] }, {}]).events).toHaveLength(2);
    expect(federateStreamRuntimes().events).toEqual([]);
    expect(buildClusterState([{}], []).worker_ids).toEqual([""]);
    const enq = enqueueExtraction([], {});
    expect(enq.enqueued).toMatch(/^task_/);
    const deq = dequeueExtraction([{ priority: undefined, order: undefined, task_id: undefined }]);
    expect(deq.task).toBeTruthy();
    const worker = createExtractionWorker(
      "w-full",
      {},
      { profile_id: "p", fingerprint_hash: "h" },
      { memory: {} },
      { events: [{ id: "e" }] },
    );
    (worker as Record<string, unknown>).adaptive_runtime = { healed_selectors: {} };
    (worker as Record<string, unknown>).stream_runtime = { events: [{ id: "s" }] };
    const out = runDistributedExtraction(
      [{ url: "https://z.test" }],
      undefined,
      { queue: [], workers: [worker], tick: 0 },
      1,
      [{ nodes: [], edges: [] }],
    );
    expect(out.bounded).toBe(true);
    expect((out.session_routes as Record<string, unknown>).routes ?? out.session_routes).toBeDefined();
  });

  it("cognition semantic vm and world model branches", () => {
    expect(runRuntimeCognitionTick({}, [], [{}, { id: "e1" }]).event_count).toBe(2);
    expect(runOntologyRuntime([{ type: "Person" }, {}]).classes).toContain("Entity");
    expect(reconcileSemanticStates([{ k: 1 }, { k: 2 }]).bounded).toBe(true);
    expect(replaySemanticEvents([]).event_count).toBe(0);
    expect(replaySemanticEvents([{ type: "x" }]).event_count).toBe(1);
    const many = Array.from({ length: 10_001 }, (_, i) => ({ opcode: "NOP", operand: { i } }));
    expect(runSemanticVm(many).executed).toBeLessThanOrEqual(10_000);
    const vm = new SemanticVirtualMachine();
    expect(vm.execute([{ opcode: "OTHER" }, { opcode: "LINK", operand: { from: "a", to: "b" } }]).executed).toBe(2);
    expect(cognizeRuntimeEnvironment({ id: "env-1", zone: "us" }).environment_id).toBe("env-1");
    expect(cognizeRuntimeEnvironment({}).environment_id).toBe("default");
    expect(buildSemanticWorldGraph({ entities: [{ id: "e" }] }).entity_count).toBe(1);
    expect(buildSemanticWorldGraph({}).entity_count).toBe(0);
    expect(compileWorldModel({ entities: [1, 2] }).entities).toHaveLength(2);
    expect(compileWorldModel({}).entities).toEqual([]);
    expect(modelOperationalTopology(buildRuntimeGraph({ a: 1 })).bounded).toBe(true);
  });

  it("evidence memory parsers connectors", () => {
    expect(validateInference({}, []).valid).toBe(false);
    expect(validateInference({ c: 1 }, ["e1"]).valid).toBe(true);
    const dir = mkdtempSync(join(tmpdir(), "wwx-mem-"));
    const path = join(dir, "mem.kaalka");
    saveRuntimeMemory(path, { runtime_history: [{ id: "h" }] }, "mem-key-90");
    expect(loadRuntimeMemory(path, "mem-key-90").runtime_history).toBeDefined();
    expect(loadRuntimeMemory(join(dir, "missing.kaalka"), "mem-key-90").memory).toBeDefined();
    rmSync(dir, { recursive: true, force: true });
    registerParser("py", { lang: "python" });
    expect(getParser("py")?.lang).toBe("python");
    expect(getParser("missing")).toBeUndefined();
    expect(listParsers().length).toBeGreaterThan(0);
    expect(extractContainerRuntime("podman").runtime).toBe("podman");
    expect(extractContainerRuntime("oci").runtime).toBe("oci");
    expect(extractContainerRuntime("unknown-runtime").degraded).toBe(true);
    const live = runLiveRuntime({}) as Record<string, unknown>;
    expect(live.bounded).toBe(true);
    expect(live.graph).toBeDefined();
    expect((live.replay as Record<string, unknown>).replayed).toBe(true);
  });
});

describe("browser branch push", () => {
  it("runtime continuation without cookies or storage", async () => {
    const session = createRuntimeSession({});
    const out = await extractWithSession("https://example.com", session, 0);
    expect(out.bounded).toBe(true);
  });
});
