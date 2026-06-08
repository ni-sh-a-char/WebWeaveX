/**
 * Converted from Python: core/distributed/distributed_scheduler_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_NODES: any = 128;
export function scheduleDistributedExecution(tasks: any, nodes: any): any {
  if (!py.truthy(nodes)) {
    nodes = ["node_a"];
  }
  var bounded_nodes: any = py.slice(py.sorted(nodes), null, MAX_NODES);
  var scheduled: any[] = [];
  var idx: any;
  var task: any;
  for ([idx, task] of py.enumerate(tasks)) {
    var node: any = py.at(bounded_nodes, py.mod(idx, py.len(bounded_nodes)));
    py.listAppend(scheduled, {"task": task, "node": node});
  }
  return {"scheduled": scheduled, "deterministic": true};
}
