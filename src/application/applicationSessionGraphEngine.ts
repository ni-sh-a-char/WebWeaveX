/**
 * Converted from Python: core/application/application_session_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildApplicationSessionGraph(states: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var index: any;
  var state: any;
  for ([index, state] of py.enumerate(states)) {
    var route: any = py.toStr(py.get(state, "route", `route_${py.toStr(index)}`));
    py.listAppend(nodes, {"id": route, "type": "session_state"});
    if ((index > 0)) {
      py.listAppend(edges, {"from": py.toStr(py.get(py.at(states, py.sub(index, 1)), "route", "")), "to": route, "relation": "session_progress"});
    }
  }
  return {"nodes": nodes, "edges": edges, "bounded": true};
}
