import { describe, expect, it } from "vitest";
import {
  buildRuntimeMemory,
  mergeRuntimeMemories,
  queryRuntimeMemory,
  replicateRuntimeMemory,
  stableMemoryHash,
} from "../../src/memory/runtimeMemory.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("runtime memory", () => {
  it("build and merge", () => {
    const g = buildRuntimeGraph({ x: 1 });
    const m1 = buildRuntimeMemory(g);
    const m2 = buildRuntimeMemory(g);
    const merged = mergeRuntimeMemories(m1, m2);
    expect(merged.stable_hash).toBeTruthy();
    expect(stableMemoryHash(g)).toBe(m1.stable_hash);
  });

  it("query replicate and empty merge", () => {
    const g = buildRuntimeGraph({ y: 2 });
    const m = buildRuntimeMemory(g, [{ t: 1 }]);
    expect(queryRuntimeMemory(m, "graph")).toBeTruthy();
    expect(replicateRuntimeMemory(m).stable_hash).toBe(m.stable_hash);
    const empty = mergeRuntimeMemories({}, {});
    expect(empty.bounded).toBe(true);
  });
});
