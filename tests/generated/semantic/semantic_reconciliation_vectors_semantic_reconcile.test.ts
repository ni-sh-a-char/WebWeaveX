import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector semantic_reconciliation_vectors/semantic-reconcile", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("semantic_reconciliation_vectors");
    const row = family.vectors.find((v) => v.id === "semantic-reconcile");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
