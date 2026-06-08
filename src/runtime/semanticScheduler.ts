/**
 * Converted from Python: core/runtime/semantic_scheduler.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function scheduleSemanticTasks(tasks: any, max_tasks: any = 32): any {
  var results: any[] = [];
  var t: any;
  for (t of py.iter(py.slice(tasks, null, max_tasks))) {
    var fn: any = py.get(t, "fn");
    if ((typeof fn === "function")) {
      py.listAppend(results, {"id": py.get(t, "id"), "result": fn(), "status": "ok"});
    } else {
      py.listAppend(results, {"id": py.get(t, "id"), "status": "skipped"});
    }
  }
  return results;
}
