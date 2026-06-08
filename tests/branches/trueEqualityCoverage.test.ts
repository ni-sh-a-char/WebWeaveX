import { describe, expect, it } from "vitest";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { synchronizeAdaptiveRuntime } from "../../src/distributed/distributedAdaptiveRuntimeEngine.js";
import { federateStreamRuntimes } from "../../src/distributed/distributedStreamEngine.js";
import { federateExtractionRuntimes } from "../../src/distributed/runtimeFederationEngine.js";
import { monitorExtractionCluster } from "../../src/distributed/distributedMonitoringEngine.js";
import { routeBrowserIdentity } from "../../src/distributed/distributedIdentityEngine.js";
import { scheduleExtractionRuntime } from "../../src/distributed/extractionSchedulerEngine.js";
import { enqueueExtraction, dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import {
  loadStreamRuntime,
  mergeStreamRuntimePayloads,
  saveStreamRuntime,
} from "../../src/streaming/streamPersistence.js";
import { makeStreamEvent } from "../../src/streaming/streamCapture.js";
import {
  executeWorkflowPlan,
  replayWorkflowRuntime,
  runAutonomousWorkflow,
} from "../../src/workflows/workflowOrchestrator.js";
import { queryRuntimeMemory } from "../../src/memory/memoryQuery.js";
import { buildRuntimeMemoryGraph } from "../../src/memory/runtimeMemoryGraph.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { buildRuntimeMemory } from "../../src/memory/runtimeMemory.js";
import { detectBuildSystems } from "../../src/repository/buildSystemDetection.js";
import { replaySemanticState } from "../../src/semantic/semanticReplay.js";
import { reconcileSemanticStates } from "../../src/semantic/semanticReconciliation.js";
import { strategyFor } from "../../src/orchestration/extractionStrategyEngine.js";
import { schedule } from "../../src/orchestration/extractionScheduler.js";
import { reconstructBrowserState } from "../../src/reconstruction/reconstructBrowser.js";
import {
  reconstructMemoryFromEnvelope,
  reconstructMemoryGraph,
} from "../../src/reconstruction/reconstructMemory.js";
import {
  graphReconstructionFingerprint,
  reconstructGraphFromSources,
  reconstructRuntimeGraph,
} from "../../src/reconstruction/reconstructGraph.js";
import {
  computeReplayFingerprint,
  validateFingerprintReplayEquivalence,
} from "../../src/replay/replayFingerprint.js";
import { replaySemanticEvents } from "../../src/runtime/semanticReplayVm.js";
import { recoverRuntime } from "../../src/runtime/runtimeRecoveryEngine.js";
import { transitionRuntimeState } from "../../src/runtime/runtimeStateMachine.js";

describe("true equality branch coverage", () => {
  it("distributed adaptive, stream, federation, and monitoring branches", () => {
    const adaptiveOnly = synchronizeAdaptiveRuntime([
      {
        adaptive_runtime: {
          healed_selectors: { "#a": "ok" },
          pagination_patterns: ["p"],
          modal_solutions: [{ id: "m" }],
        },
        schema: {},
      },
      {
        memory: { healed_selectors: { "#b": "ok" } },
        schema: { fields: ["z", "a"] },
      },
    ]);
    expect(Object.keys(adaptiveOnly.healed_selectors as object).length).toBe(2);
    expect((adaptiveOnly.stable_schema_fields as string[]).length).toBe(2);

    const nestedStream = federateStreamRuntimes([
      { worker_id: "w1", stream_runtime: { events: [{ timestamp: 2, id: "b" }] } },
      { worker_id: "w2", events: [{ timestamp: 1, id: "a" }] },
    ]);
    expect((nestedStream.events as unknown[]).length).toBe(2);

    const fed = federateExtractionRuntimes([
      { nodes: [{ id: "n1" }], edges: [] },
      { nodes: [], edges: [{ from: "a", to: "b" }] },
      {},
    ]);
    expect((fed.topology as Record<string, unknown>).nodes).toBeDefined();
    expect(federateExtractionRuntimes([]).runtime_count).toBe(0);

    expect(monitorExtractionCluster([{ status: "unknown" }], [{}, {}]).active_workers).toBe(0);
    expect((routeBrowserIdentity([{}]).routes as any[])[0]!.profile_id).toBe("default");

    const scheduled = scheduleExtractionRuntime(
      [{ retries: 2, cooldown: 3, pacing: 2, priority: 5 }],
      10,
    );
    expect((scheduled.scheduled as unknown[]).length).toBe(1);
    const enq = enqueueExtraction([{ task_id: "a", priority: 1, order: 0 }], {
      url: "https://x.test",
      priority: 2,
    });
    expect(enq.queue.length).toBe(2);
    expect(dequeueExtraction([]).task).toBeNull();
  });

  it("stream persistence merge and corrupt load branches", () => {
    const merged = mergeStreamRuntimePayloads([
      { events: [{ timestamp: 2, id: "b", source: "s", direction: "in", payload: "{}", connection_id: "c" }] },
      { events: [{ timestamp: 1, id: "a", source: "s", direction: "out", payload: "{}", connection_id: "c" }] },
      {},
    ]);
    expect(merged.stream_count).toBe(3);
    expect(merged.events[0]!.timestamp).toBeLessThanOrEqual(merged.events[1]!.timestamp ?? 0);

    const dir = mkdtempSync(join(tmpdir(), "wwx-corrupt-"));
    const path = join(dir, "bad.json");
    writeFileSync(path, "not-json");
    expect(loadStreamRuntime(path, "k").events).toEqual([]);
    const corruptEnc = join(dir, "enc.json");
    writeFileSync(corruptEnc, JSON.stringify({ encrypted: "bad" }));
    expect(loadStreamRuntime(corruptEnc, "k").events).toEqual([]);
    saveStreamRuntime(join(dir, "ok.json"), { events: [makeStreamEvent(0, "s", "in", "{}", "c")] }, "key");
    expect(loadStreamRuntime(join(dir, "ok.json"), "key").events.length).toBe(1);
    rmSync(dir, { recursive: true, force: true });
  });

  it("workflow, memory query, graph, repository, and semantic branches", () => {
    const wf = executeWorkflowPlan({
      objective: "obj",
      steps: [{ id: "s1", action: "go", runtime: "vm" }],
    });
    expect(wf.completed_count).toBe(1);
    expect((wf.executed as unknown[])).toHaveLength(1);
    expect(runAutonomousWorkflow("o").plan).toBeDefined();
    expect(replayWorkflowRuntime({ plan: { objective: "x" } }).replayed).toBe(true);

    const graph = buildRuntimeGraph({ n: 1 });
    const mem = buildRuntimeMemory(graph);
    expect(queryRuntimeMemory(mem, "graph")).toBeTruthy();
    const memGraph = buildRuntimeMemoryGraph(
      {
        nodes: [{ id: "n1", type: "t" }],
        edges: [{ from: "n1", to: "n2", type: "rel" }],
      },
      [],
    );
    expect(memGraph.relations.length).toBe(1);

    expect(
      detectBuildSystems([
        { path: "pkg/package.json" },
        { path: "py/pyproject.toml" },
        { path: "py/setup.py" },
        { path: "rs/Cargo.toml" },
        { path: "go/go.mod" },
      ]).build_systems,
    ).toEqual(["cargo", "go", "npm", "python"]);

    expect(replaySemanticState({}).replayed).toBe(true);
    expect(reconcileSemanticStates([{ a: 1 }]).count).toBe(1);
    expect(strategyFor("https://x").mode).toBe("web");
    expect(strategyFor("file").mode).toBe("web");
    expect(schedule({ extraction_order: ["https://x.test"] }).scheduled).toHaveLength(1);
  });

  it("reconstruction, replay fingerprint, and runtime state branches", () => {
    expect(reconstructBrowserState({ browser_ir: { routes: {} } } as never).tabs[0]!.path).toBe("/");
    const graph = buildRuntimeGraph({ x: 1 });
    expect(reconstructMemoryGraph(graph, [{ tick: 0 }]).bounded).toBe(true);
    expect(
      reconstructMemoryFromEnvelope({
        unified_runtime_graph: graph,
        runtime_memory: { runtime_history: [{ id: "h" }] },
      }).bounded,
    ).toBe(true);
    expect(reconstructRuntimeGraph({ graph: { nodes: [{ id: "n" }], edges: [] } }).nodes.length).toBe(1);
    expect(reconstructGraphFromSources({ z: 1, a: 2 }).nodes.length).toBe(2);
    expect(graphReconstructionFingerprint(graph)).toBeTruthy();

    const env = { dom_html: "<x/>", unified_runtime_graph: graph } as never;
    expect(computeReplayFingerprint(env, graph)).toBeTruthy();
    expect(validateFingerprintReplayEquivalence(env, env, graph).equivalent).toBe(true);

    expect(replaySemanticEvents([{ type: "ev" }]).event_count).toBe(1);
    expect(recoverRuntime("failed", ["e1", "e2"]).recovered_state).toBe("failed");
    expect(recoverRuntime("initialized").recovered_state).toBe("initialized");
    expect(transitionRuntimeState("initialized", "running").valid).toBe(true);
    expect(transitionRuntimeState("completed", "running").valid).toBe(false);
  });
});
