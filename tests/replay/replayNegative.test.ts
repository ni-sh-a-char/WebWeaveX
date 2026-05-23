import { describe, expect, it } from "vitest";
import { validateReplayEquivalence } from "../../src/replay/replayEquivalence.js";

describe("replay negative", () => {
  it("detects mismatch", () => {
    const a = {
      bounded: true,
      unified_runtime_graph: { nodes: [{ id: "1" }], edges: [] },
      browser_ir: { runtime_identity: "a" },
    };
    const b = {
      bounded: true,
      unified_runtime_graph: { nodes: [{ id: "2" }], edges: [] },
      browser_ir: { runtime_identity: "b" },
    };
    expect(validateReplayEquivalence(a, b).equivalent).toBe(false);
  });
});
