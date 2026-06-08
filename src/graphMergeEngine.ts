/**
 * Converted from Python: core/graph_merge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function mergeGraphs(graphs: any): any {
  var nodes: Set<any> = new Set();
  var edges: Set<any> = new Set();
  var max_edges: any = 0;
  var g: any;
  for (g of py.iter(py.or2(graphs, () => ([])))) {
    var n: any;
    for (n of py.iter(py.get(g, "nodes", []))) {
      var nid: any = (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) ? py.get(n, "id", "") : py.toStr(n));
      if (py.truthy(nid)) {
        py.setAdd(nodes, nid);
      }
    }
    var e: any;
    for (e of py.iter(py.get(g, "edges", []))) {
      if ((((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.contains(e, "from") && py.contains(e, "to") && !py.contains(e, "type"))) {
        py.setAdd(edges, [py.get(e, "from", ""), py.get(e, "to", "")]);
      }
    }
    max_edges = py.max([max_edges, py.toInt(py.or2(py.get(g, "max_edges", 0), () => (0)))]);
  }
  return {"nodes": py.iter(py.sorted(nodes)).map((n: any) => ({"id": n, "kind": "structural", "metadata": {}})), "edges": py.iter(py.sorted(edges)).map(([a, b]: any) => ({"from": a, "to": b})), "max_edges": max_edges};
}
