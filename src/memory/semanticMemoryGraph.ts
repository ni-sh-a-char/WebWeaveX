import { buildRuntimeMemoryGraph } from "./runtimeMemoryGraph.js";
import { buildSemanticMemory } from "../semantic/semanticMemory.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

export function buildSemanticMemoryGraph(
  graph: RuntimeGraph,
  semantic: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    memory_graph: buildRuntimeMemoryGraph(graph),
    semantic: buildSemanticMemory(semantic),
    bounded: true,
  };
}
