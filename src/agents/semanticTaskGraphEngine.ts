/**
 * Converted from Python: core/agents/semantic_task_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TASKS: any = 10000;
export function buildSemanticTaskGraph(tasks: any): any {
  var bounded: any = py.slice(tasks, null, MAX_TASKS);
  var edges: any[] = [];
  var idx: any;
  for (idx = 0; idx < py.sub(py.len(bounded), 1); idx++) {
    py.listAppend(edges, {"from": py.get(py.at(bounded, idx), "id"), "to": py.get(py.at(bounded, py.add(idx, 1)), "id")});
  }
  return {"tasks": bounded, "edges": edges};
}
