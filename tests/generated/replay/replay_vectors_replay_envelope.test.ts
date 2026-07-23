import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector replay_vectors/replay-envelope", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("replay_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "replay-envelope");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
