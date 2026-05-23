import { describe, expect, it } from "vitest";
import { rebuildExecutionGraph } from "../../src/reconstruction/reconstructRuntime.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("rebuildExecutionGraph", () => {
  it("rebuilds graph", () => {
    const g = buildRuntimeGraph({ x: 1 });
    const out = rebuildExecutionGraph({ unified_runtime_graph: g, bounded: true });
    expect(out.nodes.length).toBeGreaterThan(0);
  });
});
