/**
 * Converted from Python: core/engineering/semantic_architectural_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeArchitecturalPressure(graph: any): any {
  var node_count: any = py.len(py.get(graph, "nodes", []));
  var edge_count: any = py.len(py.get(graph, "edges", []));
  var pressure: any = py.round(py.div(edge_count, py.max([node_count, 1])), 3);
  return {"architectural_pressure": pressure, "node_count": node_count, "edge_count": edge_count};
}
