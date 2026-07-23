import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector browser_vectors/browser-graph", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("browser_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "browser-graph");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
