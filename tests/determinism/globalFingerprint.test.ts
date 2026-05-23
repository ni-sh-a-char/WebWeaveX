import { describe, expect, it } from "vitest";
import { computeGlobalRuntimeFingerprint } from "../../src/determinism/globalRuntimeFingerprint.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("globalRuntimeFingerprint extended", () => {
  it("includes memory sync reconstruction", () => {
    const g = buildRuntimeGraph({ x: 1 });
    const fp = computeGlobalRuntimeFingerprint(
      {
        bounded: true,
        pipeline_hash: "p",
        runtime: { dom_stabilization: { stabilized_hash: "d" } },
        browser_ir: { runtime_identity: "i" },
      },
      g,
      { stable_hash: "m", memory: { runtime_history: [1, 2] } },
      { convergence: { converged: true } },
      { runtime: { runtime_id: "r" } },
      "seal",
    );
    expect(fp).toHaveLength(64);
  });
});
