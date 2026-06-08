/**
 * Converted from Python: core/application/action_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildActionGraph(interactions: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var index: any;
  var action: any;
  for ([index, action] of py.enumerate(py.slice(interactions, null, 10000))) {
    var action_type: any = py.toStr(py.get(action, "action", py.get(action, "type", "action")));
    var selector: any = py.toStr(py.get(action, "selector", ""));
    var node_id: any = `action_${py.toStr(index)}`;
    py.listAppend(nodes, {"id": node_id, "type": action_type, "selector": selector});
    if ((index > 0)) {
      py.listAppend(edges, {"from": `action_${py.toStr(py.sub(index, 1))}`, "to": node_id, "relation": "sequential"});
    }
  }
  return {"nodes": nodes, "edges": edges, "bounded": true};
}
