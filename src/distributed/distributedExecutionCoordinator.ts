/**
 * Converted from Python: core/distributed/distributed_execution_coordinator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function coordinateDistributedExecution(schedules: any): any {
  var ordered: any = py.sorted(schedules, {key: ((x: any) => py.toStr(x)) as (item: any) => any});
  return {"coordinated": ordered, "count": py.len(ordered)};
}
