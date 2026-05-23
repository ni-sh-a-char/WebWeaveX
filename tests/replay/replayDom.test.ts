import { describe, expect, it } from "vitest";
import { validateReplayEquivalence } from "../../src/replay/replayEquivalence.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("replay equivalence DOM", () => {
  it("reads dom from browser_ir", () => {
    const graph = buildRuntimeGraph({ a: 1 });
    const a = {
      bounded: true,
      unified_runtime_graph: graph,
      browser_ir: { dom_html: "<p>same</p>", runtime_identity: "id-1" },
    };
    const r = validateReplayEquivalence(a, structuredClone(a));
    expect(r.checks.find((c) => c.name === "dom_stabilized_hash")?.ok).toBe(true);
  });

  it("checks stabilized dom hash when snapshot present", () => {
    const graph = buildRuntimeGraph({ a: 1 });
    const dom = '<div nonce="x">same</div>';
    const a = {
      bounded: true,
      unified_runtime_graph: graph,
      dom_snapshot: dom,
      browser_ir: { runtime_identity: "id-1" },
    };
    const b = { ...structuredClone(a), dom_snapshot: dom };
    const r = validateReplayEquivalence(a, b);
    expect(r.equivalent).toBe(true);
    expect(r.checks.some((c) => c.name === "dom_stabilized_hash")).toBe(true);
  });
});
