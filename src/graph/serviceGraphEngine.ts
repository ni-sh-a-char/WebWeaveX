/**
 * Converted from Python: core/graph/service_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildServiceGraph(services: any): any {
  var names: any = py.sorted(py.toSet(py.iter(py.or2(services, () => ([]))).filter((s: any) => py.truthy(s)).map((s: any) => py.toStr((((s !== null && typeof s === "object" && !Array.isArray(s) && !(s instanceof Set) && !(s instanceof Map))) ? py.get(s, "name") : s)))));
  var nodes: any = py.iter(names).map((n: any) => ({"id": n, "kind": "service", "metadata": {}}));
  var edges: any = py.range(py.sub(py.len(names), 1)).map((i: any) => ({"from": py.at(names, i), "to": py.at(names, py.add(i, 1))}));
  return {"nodes": nodes, "edges": edges, "max_edges": py.len(edges)};
}
