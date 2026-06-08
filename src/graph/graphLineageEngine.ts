/**
 * Converted from Python: core/graph/graph_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildLineage(graph: any): any {
  var nodes: any = py.or2(py.get(graph, "nodes", []), () => ([]));
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var stages: any = [{"stage": "graph", "nodes": py.len(nodes), "edges": py.len(edges)}];
  return {"stages": stages, "depth": py.len(stages), "node_count": py.len(nodes), "edge_count": py.len(edges)};
}
export function stampGraphLineage(graph: any, stage: any = "graph"): any {
  var lineage: any = py.or2(py.get(graph, "lineage", {}), () => ({}));
  var stages: any = ((Array.isArray(py.get(lineage, "stages"))) ? [...py.iter(py.get(lineage, "stages", []))] : []);
  py.listAppend(stages, {"stage": stage, "nodes": py.len(py.get(graph, "nodes", [])), "edges": py.len(py.get(graph, "edges", []))});
  return {...(graph), "lineage": {...(lineage), "stages": stages, "depth": py.len(stages)}};
}
