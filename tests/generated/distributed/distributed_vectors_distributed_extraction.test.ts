import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector distributed_vectors/distributed-extraction", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("distributed_vectors");
    const row = family.vectors.find((v) => v.id === "distributed-extraction");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
