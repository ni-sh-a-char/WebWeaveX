import { describe, expect, it } from "vitest";
import { loadVectorFamily } from "../../../validation/differential/common.js";

describe("vector workflow_vectors/workflow-execute", () => {
  it("loads canonical vector", () => {
    const family = loadVectorFamily("workflow_vectors");
    if (family.skip) return;
    const row = family.vectors.find((v) => v.id === "workflow-execute");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  });
});
