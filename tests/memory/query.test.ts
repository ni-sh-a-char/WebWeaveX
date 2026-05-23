import { describe, expect, it } from "vitest";
import {
  queryRuntimeMemory,
  replicateRuntimeMemory,
} from "../../src/memory/runtimeMemory.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { buildRuntimeMemory } from "../../src/memory/runtimeMemory.js";

describe("memory query", () => {
  it("query and replicate", () => {
    const m = buildRuntimeMemory(buildRuntimeGraph({ x: 1 }));
    expect(queryRuntimeMemory(m, "graph")).toBeTruthy();
    const copy = replicateRuntimeMemory(m);
    expect(copy.stable_hash).toBe(m.stable_hash);
  });
});
