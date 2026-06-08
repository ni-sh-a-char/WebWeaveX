/**
 * Converted from Python: core/graph_compression_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function compressGraph(graph: any, max_edges: any = 20000): any {
  return {"nodes": py.get(graph, "nodes", []), "edges": py.slice(py.get(graph, "edges", []), null, max_edges), "max_edges": max_edges};
}
