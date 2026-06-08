import { describe, expect, it } from "vitest";
import { runAutonomousWorkflow } from "../../src/workflows/workflowOrchestrator.js";
import { routeBrowserIdentity } from "../../src/distributed/distributedIdentityEngine.js";
import { dequeueExtraction, enqueueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { replayWorkflowRuntime } from "../../src/workflows/workflowOrchestrator.js";
import { scheduleExtractionRuntime } from "../../src/distributed/extractionSchedulerEngine.js";
import { buildParserCognitionEvidence } from "../../src/parsers/parserOrchestration.js";
import { buildSemanticGraph } from "../../src/semantic/semanticGraph.js";

describe("protected module branch coverage", () => {
  it("workflow maxSteps branches", () => {
    expect((runAutonomousWorkflow("a").plan as { steps: unknown[] }).steps).toHaveLength(3);
    expect((runAutonomousWorkflow("b").plan as { steps: unknown[] }).steps).toHaveLength(3);
    expect(replayWorkflowRuntime({}).replayed).toBe(true);
    expect(replayWorkflowRuntime({ plan: { objective: "x" } }).bounded).toBe(true);
  });

  it("distributed identity and queue branches", () => {
    expect(routeBrowserIdentity([]).routes).toEqual([]);
    expect(
      (routeBrowserIdentity([
        { worker_id: "b", identity: { fingerprint_hash: "fp" } },
        { worker_id: "a", identity: { runtime_identity: "ri" } },
        { worker_id: "c" },
      ]).routes as any[])[0]!.worker_id,
    ).toBe("a");
    expect(dequeueExtraction([]).task).toBeNull();
    expect(dequeueExtraction([{ priority: 1, task_id: "t" }]).task).toBeTruthy();
    expect(dequeueExtraction([{ priority: 2, order: 1, task_id: "b" }, { priority: 2, order: 0, task_id: "a" }]).task?.task_id).toBe("a");
    const enq = enqueueExtraction([], { url: "https://x.test", priority: 3 });
    expect(enq.enqueued).toMatch(/^task_/);
    expect(scheduleExtractionRuntime([], 0).bounded).toBe(true);
    expect(scheduleExtractionRuntime([{ id: 1 }], 2).tick).toBe(2);
  });

  it("parser and semantic graph branches", () => {
    expect(buildParserCognitionEvidence({ evidence: "x" }).bounded).toBe(true);
    expect((buildSemanticGraph([{ label: "a" }]).nodes as unknown[]).length).toBeGreaterThan(0);
    expect(buildSemanticGraph([]).nodes).toEqual([]);
  });
});
