import { describe, expect, it } from "vitest";
import {
  buildRuntimeMemory,
  mergeRuntimeMemories,
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
});
