import { describe, expect, it } from "vitest";
import { computeGlobalRuntimeFingerprint } from "../../src/determinism/globalRuntimeFingerprint.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("global fingerprint all branches", () => {
  it("spa hash and memory-only block", () => {
    const graph = buildRuntimeGraph({ a: 1 });
    const fp1 = computeGlobalRuntimeFingerprint(
      {
        runtime: { spa_stabilization: { stable_dom_hash: "spa" } },
        unified_runtime_graph: graph,
      },
      undefined,
      { memory: { runtime_history: [1] } },
    );
    const fp2 = computeGlobalRuntimeFingerprint(
      { unified_runtime_graph: graph },
      graph,
      undefined,
      undefined,
      undefined,
      "",
    );
    expect(fp1).not.toBe(fp2);
  });

  it("edges use from/to in fingerprint", () => {
    const g = {
      nodes: [{ id: "a" }, { id: "b" }],
      edges: [{ from: "a", to: "b", type: "link" }],
      bounded: true,
    };
    const fp = computeGlobalRuntimeFingerprint({ unified_runtime_graph: g }, g);
    expect(fp.length).toBe(64);
  });
});
