import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector continuation_memory_vectors/continuation-memory", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("continuation_memory_vectors");
    const row = family.vectors.find((v) => v.id === "continuation-memory");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
