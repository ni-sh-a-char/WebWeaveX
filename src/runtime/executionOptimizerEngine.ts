/**
 * Converted from Python: core/runtime/execution_optimizer_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function optimizeExecutionOrder(tasks: any): any {
  var ordered: any = py.sorted(tasks, {key: ((x: any) => [py.get(x, "weight", 0), py.get(x, "priority", 0)]) as (item: any) => any});
  return {"tasks": ordered, "optimized": true};
}
