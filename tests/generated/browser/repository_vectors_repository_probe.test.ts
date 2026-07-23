import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector repository_vectors/repository-probe", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("repository_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "repository-probe");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
