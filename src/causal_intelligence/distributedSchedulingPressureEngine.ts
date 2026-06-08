/**
 * Converted from Python: core/causal_intelligence/distributed_scheduling_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SCHEDULING_PRESSURE: any = 100000;
export function computeSchedulingPressure(runtime_ir: any): any {
  var tasks: any = [...py.iter(py.or2(py.get(runtime_ir, "tasks", []), () => ([])))];
  var workers: any = [...py.iter(py.or2(py.get(runtime_ir, "distributed_workers", []), () => ([])))];
  var pressure: any = py.min([py.mul(py.len(tasks), py.max([py.len(workers), 1])), MAX_SCHEDULING_PRESSURE]);
  return {"scheduling_pressure": pressure, "task_count": py.len(tasks), "bounded": true};
}
