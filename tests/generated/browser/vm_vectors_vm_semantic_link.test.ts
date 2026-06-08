import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector vm_vectors/vm-semantic-link", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("vm_vectors");
    const row = family.vectors.find((v) => v.id === "vm-semantic-link");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
