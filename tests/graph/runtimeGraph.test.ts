import { describe, expect, it } from "vitest";
import {
  buildRuntimeGraph,
  graphFingerprint,
  queryRuntimeGraph,
} from "../../src/graph/runtimeGraph.js";

describe("runtimeGraph", () => {
  it("build query fingerprint", () => {
    const g = buildRuntimeGraph({ a: 1, b: 2 });
    expect(g.nodes.length).toBe(2);
    const q = queryRuntimeGraph(g, "a");
    expect(q.nodes.length).toBe(1);
    expect(graphFingerprint(g)).toHaveLength(64);
  });
});
