import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";

export function buildUnifiedRuntimeIR(parts: {
  extraction?: ExtractionEnvelope;
  memory?: Record<string, unknown>;
  reconstruction?: Record<string, unknown>;
}): Record<string, unknown> {
  const graph = RuntimeGraphContract.normalize(
    (parts.extraction?.unified_runtime_graph as RuntimeGraph) ?? { nodes: [], edges: [] },
  );
  return {
    ir_version: "2.0.0",
    graph,
    memory: parts.memory ?? {},
    reconstruction: parts.reconstruction ?? {},
    bounded: true,
  };
}

export function compileRuntimeIR(ir: Record<string, unknown>): Record<string, unknown> {
  const graph = RuntimeGraphContract.normalize((ir.graph as RuntimeGraph) ?? { nodes: [], edges: [] });
  return { ...ir, graph, compiled: true, bounded: true };
}
