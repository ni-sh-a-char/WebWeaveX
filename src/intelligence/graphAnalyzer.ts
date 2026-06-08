/**
 * Converted from Python: core/intelligence/graph_analyzer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function analyzeGraph(nodes: any, edges: any): any {
  var n: any = py.len(nodes);
  var e: any = py.len(edges);
  var density: any = py.F(0.0);
  if ((n > 1)) {
    density = py.div(e, py.mul(n, py.sub(n, 1)));
  }
  var degree: Record<string, any> = {};
  var node: any;
  for (node of py.iter(nodes)) {
    var node_id: any = py.get(node, "id", "");
    if (py.truthy(node_id)) {
      py.setItem(degree, node_id, 0);
    }
  }
  var edge: any;
  for (edge of py.iter(edges)) {
    var f: any = py.get(edge, "from", "");
    var t: any = py.get(edge, "to", "");
    if (py.contains(degree, f)) {
      py.setItem(degree, f, py.add(py.at(degree, f), 1));
    }
    if (py.contains(degree, t)) {
      py.setItem(degree, t, py.add(py.at(degree, t), 1));
    }
  }
  return {"node_count": n, "edge_count": e, "density": density, "degree_map": py.pyDict(py.sorted(py.items(degree)))};
}
