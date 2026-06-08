import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector distributed_replay_vectors/distributed-replay", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("distributed_replay_vectors");
    const row = family.vectors.find((v) => v.id === "distributed-replay");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
