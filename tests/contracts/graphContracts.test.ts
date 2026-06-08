import { describe, expect, it } from "vitest";
import { RuntimeGraphContract } from "../../src/contracts/graphContracts.js";

describe("RuntimeGraphContract", () => {
  it("normalizes nodes and edges with alternate keys", () => {
    const g = RuntimeGraphContract.normalize({
      nodes: [
        { type: "b", name: "two" },
        { id: "a", type: "a", name: "one" },
      ],
      edges: [
        { from: "a", to: "b", type: "link" },
        { source: "b", target: "c", type: "other" },
      ],
    });
    expect(g.nodes.map((n: any) => n.id)).toContain("a");
    expect(g.edges.length).toBe(2);
    expect(g.bounded).toBe(true);
  });
});
