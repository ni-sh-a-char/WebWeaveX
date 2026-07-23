import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector graph_vectors/graph-step", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("graph_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "graph-step");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
