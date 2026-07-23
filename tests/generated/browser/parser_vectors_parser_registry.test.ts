import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector parser_vectors/parser-registry", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("parser_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "parser-registry");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
