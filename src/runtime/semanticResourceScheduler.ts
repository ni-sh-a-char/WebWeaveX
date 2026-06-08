/**
 * Converted from Python: core/runtime/semantic_resource_scheduler.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function scheduleSemanticResources(tasks: any): any {
  var ordered: any = py.sorted(tasks, {key: ((x: any) => py.toStr(py.get(x, "priority", 0))) as (item: any) => any});
  return {"scheduled": ordered, "count": py.len(ordered)};
}
