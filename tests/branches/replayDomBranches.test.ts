import { describe, expect, it } from "vitest";
import { validateReplayEquivalence } from "../../src/replay/replayEquivalence.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("replay equivalence branches", () => {
  it("dom payloads still produce exactly the three authority checks", () => {
    const g = buildRuntimeGraph({ n: 1 });
    const a = { unified_runtime_graph: g, dom_html: "<div/>" } as never;
    const b = { unified_runtime_graph: g, dom_html: "<div/>" } as never;
    const r = validateReplayEquivalence(a, b);
    expect(r.equivalent).toBe(true);
    expect(r.checks.length).toBe(3);
  });

  it("different browser identity", () => {
    const g = buildRuntimeGraph({ n: 1 });
    const a = { unified_runtime_graph: g, browser_ir: { runtime_identity: "a" } } as never;
    const b = { unified_runtime_graph: g, browser_ir: { runtime_identity: "b" } } as never;
    expect(validateReplayEquivalence(a, b).equivalent).toBe(false);
  });
});
