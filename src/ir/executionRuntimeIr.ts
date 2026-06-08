/**
 * Converted from Python: core/ir/execution_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileExecutionRuntimeIr(execution_payload: any): any {
  return {"ir": "execution_runtime", "actions": py.get(execution_payload, "actions", []), "queues": py.get(execution_payload, "queue", {}), "transactions": py.get(execution_payload, "transactions", []), "mutations": py.get(execution_payload, "mutations", {}), "checkpoints": py.get(execution_payload, "checkpoints", []), "federation": py.get(execution_payload, "federation", {}), "synchronization": py.get(execution_payload, "synchronization", {}), "execution_state": py.get(execution_payload, "state", {}), "coordination": py.get(execution_payload, "coordination", {}), "simulation": py.get(execution_payload, "simulation", {}), "bounded": true};
}
export function executionRuntimeIrToGraph(execution_ir: any): any {
  var nodes: any = [{"id": "execution:root", "type": "execution", "runtime": "operational"}];
  var edges: any[] = [];
  var action: any;
  for (action of py.iter(py.slice(py.get(execution_ir, "actions", []), null, 10000))) {
    var action_id: any = py.toStr(py.get(action, "id", py.get(action, "action_id", "")));
    if (!py.truthy(action_id)) {
      continue;
    }
    py.listAppend(nodes, {"id": `action:${py.toStr(action_id)}`, "type": "action"});
    py.listAppend(edges, {"from": "execution:root", "to": `action:${py.toStr(action_id)}`, "relation": "executes"});
  }
  var route: any;
  for (route of py.iter(py.slice(py.get(py.get(execution_ir, "federation", {}), "execution_routes", []), null, 10000))) {
    var worker_id: any = py.toStr(py.get(route, "worker_id", ""));
    if (py.truthy(worker_id)) {
      py.listAppend(nodes, {"id": `worker:${py.toStr(worker_id)}`, "type": "worker"});
      py.listAppend(edges, {"from": `worker:${py.toStr(worker_id)}`, "to": "execution:root", "relation": "coordinates"});
    }
  }
  var mutation: any;
  for (mutation of py.iter(py.slice(py.get(py.get(execution_ir, "mutations", {}), "mutations", []), null, 10000))) {
    var target: any = py.toStr(py.get(mutation, "target", py.get(mutation, "kind", "mutation")));
    var node_id: any = `mutation:${py.toStr(target)}`;
    py.listAppend(nodes, {"id": node_id, "type": "mutation"});
    py.listAppend(edges, {"from": node_id, "to": "execution:root", "relation": "mutates"});
  }
  return {"ir": "execution_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
