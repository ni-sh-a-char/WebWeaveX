import { describe, expect, it } from "vitest";
import {
  normalizeRuntimeGraph,
  normalizeRuntimeState,
} from "../../src/determinism/normalization.js";

describe("normalizeRuntime", () => {
  it("strips volatile keys", () => {
    const s = normalizeRuntimeState({ timestamp: 1, ok: { nested: true } });
    expect(s.timestamp).toBeUndefined();
    expect((s.ok as Record<string, unknown>).nested).toBe(true);
  });

  it("normalizes graph", () => {
    const g = normalizeRuntimeGraph({ nodes: [{ id: "b" }, { id: "a" }], edges: [] });
    expect(g.nodes[0]?.id).toBe("a");
  });
});
