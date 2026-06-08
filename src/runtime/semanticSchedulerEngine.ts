/**
 * Converted from Python: core/runtime/semantic_scheduler_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";
import { DEFAULT_RUNTIME_BUDGET } from "./runtimeBudgetEngine.js";

export function scheduleSemanticRuntimeTasks(tasks: any): any {
  var ordered: any = py.sorted(tasks, {key: ((t: any) => [py.toInt(py.get(t, "priority", 0)), py.toStr(py.get(t, "id", ""))]) as (item: any) => any});
  var bounded: any = py.slice(ordered, null, DEFAULT_RUNTIME_BUDGET.max_tasks);
  return {"scheduled": py.iter(bounded).map((t: any) => ({"id": py.get(t, "id"), "priority": py.get(t, "priority", 0)})), "dropped": py.max([0, py.sub(py.len(ordered), py.len(bounded))]), "deterministic": true, "bounded": true};
}
export { DEFAULT_RUNTIME_BUDGET };
