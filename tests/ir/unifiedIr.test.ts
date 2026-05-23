import { describe, expect, it } from "vitest";
import { buildUnifiedRuntimeIR, compileRuntimeIR } from "../../src/ir/unifiedIr.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("unified IR", () => {
  it("build and compile", () => {
    const graph = buildRuntimeGraph({ web: { u: 1 } });
    const ir = buildUnifiedRuntimeIR({ extraction: { unified_runtime_graph: graph } });
    const compiled = compileRuntimeIR(ir);
    expect(compiled.compiled).toBe(true);
  });
});
