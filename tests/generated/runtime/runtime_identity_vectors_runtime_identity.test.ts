import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector runtime_identity_vectors/runtime-identity", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("runtime_identity_vectors");
    const row = family.vectors.find((v) => v.id === "runtime-identity");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
