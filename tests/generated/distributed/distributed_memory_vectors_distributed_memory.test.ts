import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector distributed_memory_vectors/distributed-memory", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("distributed_memory_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "distributed-memory");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
