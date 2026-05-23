import { describe, expect, it } from "vitest";
import { validateReplayEquivalence } from "../../src/replay/replayEquivalence.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("validateReplayEquivalence", () => {
  it("equivalent graphs match", () => {
    const graph = buildRuntimeGraph({ a: { x: 1 } });
    const original = {
      bounded: true,
      unified_runtime_graph: graph,
      browser_ir: { runtime_identity: "id-1" },
      pipeline_hash: "ph",
    };
    const replayed = structuredClone(original);
    const result = validateReplayEquivalence(original, replayed);
    expect(result.equivalent).toBe(true);
  });
});
