import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector semantic_vectors/semantic-ontology", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("semantic_vectors");
    const row = family.vectors.find((v) => v.id === "semantic-ontology");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
