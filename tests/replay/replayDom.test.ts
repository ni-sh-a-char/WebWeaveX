import { describe, expect, it } from "vitest";
import { validateReplayEquivalence } from "../../src/replay/replayEquivalence.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("replay equivalence DOM", () => {
  it("envelopes with browser_ir compare via the three authority checks", () => {
    const graph = buildRuntimeGraph({ a: 1 });
    const a = {
      bounded: true,
      unified_runtime_graph: graph,
      browser_ir: { dom_html: "<p>same</p>", runtime_identity: "id-1" },
    };
    const r = validateReplayEquivalence(a, structuredClone(a));
    expect(r.equivalent).toBe(true);
    expect(r.checks.map((c) => c.name)).toEqual(["graph_hash", "global_fingerprint", "browser_identity"]);
  });

  it("dom snapshots do not add extra checks (authority has exactly three)", () => {
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
    expect(r.checks.length).toBe(3);
  });
});
