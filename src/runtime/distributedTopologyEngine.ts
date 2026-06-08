/**
 * Converted from Python: core/runtime/distributed_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function buildDistributedTopology(services: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var svc: any;
  for (svc of py.iter(services)) {
    py.listAppend(nodes, {"id": svc, "type": "service"});
  }
  var i: any;
  for (i = 0; i < py.sub(py.len(services), 1); i++) {
    py.listAppend(edges, {"from": py.at(services, i), "to": py.at(services, py.add(i, 1)), "relation": "distributed_dependency"});
  }
  return {"nodes": nodes, "edges": edges, "bounded": true};
}
