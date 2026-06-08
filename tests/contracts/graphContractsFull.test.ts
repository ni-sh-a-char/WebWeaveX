import { describe, expect, it } from "vitest";
import { RuntimeGraphContract } from "../../src/contracts/graphContracts.js";

describe("RuntimeGraphContract full branches", () => {
  it("normalizes sparse nodes and mixed edges", () => {
    const g = RuntimeGraphContract.normalize({
      nodes: [
        { id: "only-id" },
        { type: "only-type" },
        { name: "only-name" },
        {},
      ],
      edges: [
        { source: "a", target: "b" },
        { from: "c", to: "d" },
        { source: "e", target: "f", type: "t" },
        {},
      ],
    });
    expect(g.nodes.length).toBe(4);
    expect(g.edges.length).toBe(4);
  });
});
