import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector memory_vectors/memory-history", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("memory_vectors");
    const row = family.vectors.find((v) => v.id === "memory-history");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
