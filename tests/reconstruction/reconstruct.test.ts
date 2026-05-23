import { describe, expect, it } from "vitest";
import { reconstructRuntime, replayRuntime } from "../../src/reconstruction/reconstructRuntime.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("reconstruction", () => {
  it("deterministic runtime_id", () => {
    const graph = buildRuntimeGraph({ a: 1 });
    const r1 = reconstructRuntime({ extraction: { unified_runtime_graph: graph } });
    const r2 = reconstructRuntime({ extraction: { unified_runtime_graph: graph } });
    expect((r1.runtime as Record<string, string>).runtime_id).toBe(
      (r2.runtime as Record<string, string>).runtime_id,
    );
  });

  it("replay clone", () => {
    const ex = { bounded: true, pipeline_hash: "x" };
    expect(replayRuntime(ex)).toEqual(ex);
  });
});
