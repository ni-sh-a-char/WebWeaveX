import { buildRuntimeMemory } from "../memory/runtimeMemory.js";
import { buildRuntimeMemoryGraph } from "../memory/runtimeMemoryGraph.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

export function reconstructMemoryGraph(
  graph: RuntimeGraph,
  history: unknown[] = [],
): Record<string, unknown> {
  const memoryGraph = buildRuntimeMemoryGraph(graph, history);
  const fabric = buildRuntimeMemory(graph, history);
  return {
    memory_graph: memoryGraph,
    memory: fabric.memory,
    stable_hash: fabric.stable_hash,
    bounded: true,
  };
}

export function reconstructMemoryFromEnvelope(
  envelope: Record<string, unknown>,
): Record<string, unknown> {
  const graph = (envelope.unified_runtime_graph ?? { nodes: [], edges: [] }) as RuntimeGraph;
  const history =
    ((envelope.runtime_memory as Record<string, unknown> | undefined)?.runtime_history as unknown[]) ??
    [];
  return reconstructMemoryGraph(graph, history);
}
