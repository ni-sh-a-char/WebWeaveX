/**
 * Converted from Python: core/runtime/distributed_routing_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function routeSemanticTasks(tasks: any, nodes: any): any {
  var routed: any[] = [];
  if (!py.truthy(nodes)) {
    return {"routes": []};
  }
  var index: any = 0;
  var task: any;
  for (task of py.iter(tasks)) {
    py.listAppend(routed, {"task": task, "node": py.at(nodes, index)});
    index = py.mod(py.add(index, 1), py.len(nodes));
  }
  return {"routes": routed};
}
