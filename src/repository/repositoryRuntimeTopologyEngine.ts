/**
 * Converted from Python: core/repository/repository_runtime_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_NODES: any = 10000;
export function buildRuntimeTopology(services: any, infra: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var svc: any;
  for (svc of py.iter(py.get(services, "services", []))) {
    py.listAppend(nodes, {"id": py.at(svc, "file"), "type": "service"});
  }
  var item: any;
  for (item of py.iter(py.get(infra, "infra", []))) {
    py.listAppend(nodes, {"id": py.at(item, "file"), "type": py.at(item, "type")});
    py.listAppend(edges, {"from": py.at(item, "file"), "to": py.at(item, "type"), "relation": "infra_signal"});
  }
  return {"nodes": py.slice(py.sorted(nodes, {key: ((x: any) => py.at(x, "id")) as (item: any) => any}), null, MAX_NODES), "edges": py.sorted(edges, {key: ((x: any) => [py.toStr(py.get(x, "from")), py.toStr(py.get(x, "to"))]) as (item: any) => any}), "bounded": true};
}
