import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector runtime_vectors/runtime-memory", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("runtime_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "runtime-memory");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
