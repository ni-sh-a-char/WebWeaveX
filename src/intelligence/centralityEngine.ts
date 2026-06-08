/**
 * Converted from Python: core/intelligence/centrality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeCentrality(nodes: any, edges: any): any {
  var degree: Record<string, any> = {};
  var node: any;
  for (node of py.iter(nodes)) {
    var node_id: any = py.get(node, "id", "");
    if (py.truthy(node_id)) {
      py.setItem(degree, node_id, {"in": 0, "out": 0});
    }
  }
  var edge: any;
  for (edge of py.iter(edges)) {
    var f: any = py.get(edge, "from", "");
    var t: any = py.get(edge, "to", "");
    if (py.contains(degree, f)) {
      py.setItem(py.at(degree, f), "out", py.add(py.at(py.at(degree, f), "out"), 1));
    }
    if (py.contains(degree, t)) {
      py.setItem(py.at(degree, t), "in", py.add(py.at(py.at(degree, t), "in"), 1));
    }
  }
  var scored: any[] = [];
  var d: any;
  for ([node, d] of py.items(degree)) {
    var score: any = py.add(py.at(d, "in"), py.at(d, "out"));
    py.listAppend(scored, [node, score]);
  }
  var ranked: any = py.sorted(scored, {key: ((x: any) => [(-py.at(x, 1)), py.at(x, 0)]) as (item: any) => any});
  return py.iter(ranked).map(([node, score]: any) => ({"id": node, "score": score}));
}
