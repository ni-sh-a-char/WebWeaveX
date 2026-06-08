/**
 * Converted from Python: core/evolution/semantic_structural_heuristics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeStructuralHeuristics(graph: any): any {
  var node_count: any = py.len(py.get(graph, "nodes", []));
  var edge_count: any = py.len(py.get(graph, "edges", []));
  return {"node_count": node_count, "edge_count": edge_count, "density": py.round(py.div(edge_count, py.max([node_count, 1])), 3)};
}
