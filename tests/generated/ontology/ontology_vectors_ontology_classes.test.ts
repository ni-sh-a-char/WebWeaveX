import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector ontology_vectors/ontology-classes", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("ontology_vectors");
    const row = family.vectors.find((v) => v.id === "ontology-classes");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
