/**
 * Converted from Python: core/application/workflow_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWorkflowGraph(states: any, transitions: any, actions: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var index: any;
  var state: any;
  for ([index, state] of py.enumerate(py.slice(states, null, 5000))) {
    var route: any = py.toStr(py.get(state, "route", `state_${py.toStr(index)}`));
    py.listAppend(nodes, {"id": route, "type": "page"});
  }
  var transition: any;
  for (transition of py.iter(py.slice(transitions, null, 10000))) {
    py.listAppend(edges, {"from": py.toStr(py.get(transition, "from", "")), "to": py.toStr(py.get(transition, "to", "")), "relation": py.toStr(py.get(transition, "relation", "transition"))});
  }
  var action: any;
  for (action of py.iter(py.slice(actions, null, 10000))) {
    var action_type: any = py.toStr(py.get(action, "action", py.get(action, "type", "")));
    var relation: any = "submit";
    if (py.eq(action_type, "click")) {
      relation = "navigate";
    } else if (py.contains(action_type, "modal")) {
      relation = "open_modal";
    }
    py.listAppend(edges, {"from": py.toStr(py.get(action, "from", "")), "to": py.toStr(py.get(action, "to", "")), "relation": relation});
  }
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
