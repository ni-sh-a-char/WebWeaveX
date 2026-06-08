/**
 * Converted from Python: core/evolution_runtime/runtime_evolution_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeEvolutionGraph(evolution: any, repairs: any, optimization: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var evolution_id: any = py.toStr(py.get(evolution, "evolution_id", "evolution:root"));
  py.listAppend(nodes, {"id": evolution_id, "type": "evolution"});
  var mutation: any;
  for (mutation of py.iter(py.slice(py.get(evolution, "mutations", []), null, 5000))) {
    var node_id: any = `mutation:${py.toStr(py.get(mutation, "kind"))}:${py.toStr(py.get(mutation, "target"))}`;
    py.listAppend(nodes, {"id": node_id, "type": "mutation"});
    py.listAppend(edges, {"from": evolution_id, "to": node_id, "relation": "evolves"});
  }
  var repair: any;
  for (repair of py.iter(py.slice(py.get(repairs, "repairs", []), null, 5000))) {
    node_id = `repair:${py.toStr(py.get(repair, "action", ""))}`;
    py.listAppend(nodes, {"id": node_id, "type": "repair"});
    py.listAppend(edges, {"from": node_id, "to": evolution_id, "relation": "repairs"});
  }
  var opt_id: any = "optimization:root";
  py.listAppend(nodes, {"id": opt_id, "type": "optimization"});
  py.listAppend(edges, {"from": opt_id, "to": evolution_id, "relation": "optimizes"});
  py.listAppend(edges, {"from": evolution_id, "to": evolution_id, "relation": "converges"});
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
