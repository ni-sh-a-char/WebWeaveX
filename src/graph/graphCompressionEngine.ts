/**
 * Converted from Python: core/graph/graph_compression_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { MAX_EDGES, reconstructGraph } from "./graphReconstructionEngine.js";

export function compressGraph(graph: any, max_edges: any = MAX_EDGES): any {
  var rebuilt: any = reconstructGraph(graph, max_edges);
  return rebuilt;
}
export { MAX_EDGES, reconstructGraph };
