/**
 * Converted from Python: core/workflows/workflow_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWorkflowGraph(objective: any, plan: any, state: any, execution: any, transitions: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var obj_name: any = py.toStr(py.get(objective, "objective", "objective"));
  py.listAppend(nodes, {"id": `objective:${py.toStr(obj_name)}`, "type": "objective"});
  var step: any;
  for (step of py.iter(py.slice(py.get(plan, "steps", []), null, 10000))) {
    var step_id: any = py.toStr(py.get(step, "id", ""));
    py.listAppend(nodes, {"id": step_id, "type": "step", "runtime": py.toStr(py.get(step, "runtime", ""))});
    var depends_on: any = py.toStr(py.get(step, "depends_on", ""));
    if (py.truthy(depends_on)) {
      py.listAppend(edges, {"from": depends_on, "to": step_id, "relation": "depends_on"});
    }
    py.listAppend(edges, {"from": `objective:${py.toStr(obj_name)}`, "to": step_id, "relation": "executes"});
  }
  var transition: any;
  for (transition of py.iter(py.slice(transitions, null, 10000))) {
    py.listAppend(edges, {"from": py.toStr(py.get(transition, "from", "")), "to": py.toStr(py.get(transition, "to", "")), "relation": "transitions"});
  }
  if ((py.get(state, "retries", 0) > 0)) {
    py.listAppend(nodes, {"id": "checkpoint:recovery", "type": "checkpoint"});
    py.listAppend(edges, {"from": "checkpoint:recovery", "to": `objective:${py.toStr(obj_name)}`, "relation": "recovers"});
  }
  py.listAppend(nodes, {"id": "semantic:state", "type": "semantic_state"});
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
