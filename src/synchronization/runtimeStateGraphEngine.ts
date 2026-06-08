/**
 * Converted from Python: core/synchronization/runtime_state_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeStateGraph(snapshot: any, delta: any, convergence: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var snapshot_id: any = py.toStr(py.get(snapshot, "snapshot_id", "snapshot:0"));
  py.listAppend(nodes, {"id": snapshot_id, "type": "snapshot"});
  var delta_id: any = py.toStr(py.get(delta, "delta_id", "delta:0"));
  py.listAppend(nodes, {"id": delta_id, "type": "delta"});
  py.listAppend(edges, {"from": snapshot_id, "to": delta_id, "relation": "mutates"});
  var change: any;
  for (change of py.iter(py.slice(py.get(delta, "changes", []), null, 5000))) {
    var node_id: any = `change:${py.toStr(py.get(change, "field", ""))}`;
    py.listAppend(nodes, {"id": node_id, "type": "mutation"});
    py.listAppend(edges, {"from": delta_id, "to": node_id, "relation": "propagates"});
  }
  var converged_id: any = "convergence:root";
  py.listAppend(nodes, {"id": converged_id, "type": "convergence"});
  py.listAppend(edges, {"from": delta_id, "to": converged_id, "relation": "converges"});
  if (py.truthy(py.get(delta, "changes"))) {
    py.listAppend(edges, {"from": converged_id, "to": snapshot_id, "relation": "synchronizes"});
  }
  py.listAppend(nodes, {"id": "checkpoint:sync", "type": "checkpoint"});
  py.listAppend(edges, {"from": converged_id, "to": "checkpoint:sync", "relation": "restores"});
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
