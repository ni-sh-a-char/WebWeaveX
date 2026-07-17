import { describe, expect, it } from "vitest";
import {
  computeDeterministicHash,
  computeDeterministicHashPayload,
  normalizeRuntimeValue,
} from "../../src/crypto/kaalkaRuntime.js";
import {
  buildUnifiedRuntimeIR,
  compileRuntimeIR,
  computeGlobalRuntimeFingerprint,
  graphFingerprint,
  normalizeRuntimeGraph,
  normalizeRuntimeState,
  runExecutionRuntime,
  VERSION,
} from "../../src/index.js";
// dict-based internal helpers (graph/runtimeGraph) — the public barrel now
// exposes the spec list-based build/query (core.runtime_graph) instead.
import { buildRuntimeGraph, queryRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("integration exports", () => {
  it("kaalka + determinism + graph utilities", () => {
    expect(VERSION).toBe("3.0.0");
    expect(normalizeRuntimeValue("a\r\n")).toBe("a");
    expect(computeDeterministicHash("x")).toHaveLength(64);
    expect(computeDeterministicHashPayload({ z: 1 })).toHaveLength(64);
    const g = buildRuntimeGraph({ a: 1, b: 2 });
    expect(graphFingerprint(g)).toHaveLength(64);
    expect(queryRuntimeGraph(g, "a").nodes.length).toBe(1);
    expect(normalizeRuntimeGraph(g).bounded).toBe(true);
    expect(normalizeRuntimeState({ timestamp: 1, ok: true }).timestamp).toBeUndefined();
    const ir = buildUnifiedRuntimeIR({ extraction: { unified_runtime_graph: g, bounded: true } });
    expect(compileRuntimeIR(ir).compiled).toBe(true);
    expect(computeGlobalRuntimeFingerprint({ bounded: true }, g)).toHaveLength(64);
    const exec = runExecutionRuntime([{ action: "checkpoint" }, { action: "bad" }]);
    expect(exec.denied).toContain("bad");
  });
});
