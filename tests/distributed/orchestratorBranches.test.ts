import { describe, expect, it } from "vitest";
import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";
import { createExtractionWorker } from "../../src/distributed/extractionWorkerEngine.js";

describe("distributed extraction branches", () => {
  it("uses checkpoint workers and runtime graphs", () => {
    const worker = createExtractionWorker(
      "w-check",
      { session: { session_fingerprint: "fp" } },
      { profile_id: "p", fingerprint_hash: "h" },
      { memory: { healed_selectors: { "#a": "ok" } } },
      { events: [{ id: "e1" }] },
    );
    const graph = { nodes: [{ id: "n1" }], edges: [], bounded: true };
    const out = runDistributedExtraction(
      [{ task_id: "t1", url: "https://a.test", priority: 2 }],
      [worker],
      { queue: [], workers: [worker], tick: 1 },
      2,
      [graph],
    );
    expect(out.bounded).toBe(true);
    expect((out.distributed_graph as Record<string, unknown>).nodes).toBeDefined();
    expect(((out.assignments as Record<string, unknown>).assignments as unknown[]).length).toBeGreaterThan(0);
  });

  it("creates default worker when none supplied", () => {
    const out = runDistributedExtraction([{ task_id: "t2", url: "https://b.test" }]);
    expect((out.workers as unknown[]).length).toBeGreaterThan(0);
  });
});
