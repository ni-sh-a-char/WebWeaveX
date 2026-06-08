/**
 * Converted from Python: core/runtime/semantic_execution_planner.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function buildExecutionPlan(tasks: any): any {
  var ordered: any = py.sorted(tasks, {key: ((x: any) => py.get(x, "priority", 0)) as (item: any) => any});
  return {"plan": ordered, "task_count": py.len(ordered), "deterministic": true};
}
