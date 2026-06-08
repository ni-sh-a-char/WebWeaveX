import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector orchestration_vectors/orchestration-extract", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("orchestration_vectors");
    const row = family.vectors.find((v) => v.id === "orchestration-extract");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
