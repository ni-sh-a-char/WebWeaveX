/**
 * Converted from Python: core/graph/reasoning/graph_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { boundGraphMemory } from "../graphReconstructionEngine.js";

export function graphMemoryBound(graph: any, max_nodes: any = 5000, max_edges: any = 20000): any {
  return boundGraphMemory(graph, max_nodes, max_edges);
}
export { boundGraphMemory };
