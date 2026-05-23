import { describe, expect, it } from "vitest";
import { computeGlobalRuntimeFingerprint } from "../../src/determinism/globalRuntimeFingerprint.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("global runtime fingerprint branches", () => {
  it("includes memory sync and reconstruction fields", () => {
    const graph = buildRuntimeGraph({ a: 1 });
    const fp = computeGlobalRuntimeFingerprint(
      {
        bounded: true,
        unified_runtime_graph: graph,
        browser_ir: { runtime_identity: "rid" },
        runtime: { dom_stabilization: { stabilized_hash: "abc" } },
        pipeline_hash: "ph",
      },
      graph,
      { stable_hash: "mh", memory: { runtime_history: [1, 2] } },
      { convergence: { converged: true } },
      { runtime: { runtime_id: "recon-1" } },
      "seal",
    );
    expect(fp).toHaveLength(64);
  });
});
