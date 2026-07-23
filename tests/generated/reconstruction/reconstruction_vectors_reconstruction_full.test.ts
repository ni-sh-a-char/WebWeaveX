import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector reconstruction_vectors/reconstruction-full", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("reconstruction_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "reconstruction-full");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
