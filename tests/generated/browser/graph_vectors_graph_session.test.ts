import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector graph_vectors/graph-session", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("graph_vectors");
    const row = family.vectors.find((v) => v.id === "graph-session");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
