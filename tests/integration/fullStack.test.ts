import { describe, expect, it } from "vitest";
import {
  computeDeterministicHash,
  computeDeterministicHashPayload,
  normalizeRuntimeValue,
} from "kaalka";
import {
  buildUnifiedRuntimeIR,
  compileRuntimeIR,
  computeGlobalRuntimeFingerprint,
  graphFingerprint,
  normalizeRuntimeGraph,
  normalizeRuntimeState,
  queryRuntimeGraph,
  runExecutionRuntime,
  VERSION,
} from "../../src/index.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("integration exports", () => {
  it("kaalka + determinism + graph utilities", () => {
    expect(VERSION).toBe("2.0.0");
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
