/**
 * Converted from Python: core/repository/distributed_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDistributedGraph(services: any, dependencies: any): any {
  var svc: any = py.sorted(py.toSet(py.or2(services, () => ([]))));
  var dep: any = py.sorted(py.toSet(py.or2(dependencies, () => ([]))));
  var edges: any[] = [];
  var s: any;
  for (s of py.iter(svc)) {
    var d: any;
    for (d of py.iter(py.slice(dep, null, 5))) {
      py.listAppend(edges, {"from": s, "to": d});
    }
  }
  return {"nodes": py.sorted(py.toSet(py.add(svc, dep))), "edges": py.sorted(edges, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any})};
}
