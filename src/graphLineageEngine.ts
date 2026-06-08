/**
 * Converted from Python: core/graph_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function graphLineage(graph: any): any {
  return {"node_count": py.len(py.get(graph, "nodes", [])), "edge_count": py.len(py.get(graph, "edges", []))};
}
