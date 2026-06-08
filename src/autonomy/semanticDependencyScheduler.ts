/**
 * Converted from Python: core/autonomy/semantic_dependency_scheduler.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function scheduleSemanticDependencies(tasks: any): any {
  var ordered: any = py.sorted(tasks, {key: ((x: any) => py.toStr(py.get(x, "id"))) as (item: any) => any});
  return {"schedule": ordered, "count": py.len(ordered)};
}
