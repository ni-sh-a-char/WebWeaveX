/**
 * Converted from Python: core/execution_reality/runtime_queue_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_QUEUE_PRESSURE: any = 100000;
export function measureQueuePressure(runtime_ir: any): any {
  var tasks: any = [...py.iter(py.or2(py.get(runtime_ir, "tasks", []), () => ([])))];
  var workers: any = [...py.iter(py.or2(py.get(runtime_ir, "distributed_workers", []), () => ([])))];
  var queue_depth: any = py.len(tasks);
  var worker_count: any = py.max([py.len(workers), 1]);
  var pressure: any = py.min([py.mul(queue_depth, worker_count), MAX_QUEUE_PRESSURE]);
  return {"queue_depth": queue_depth, "queue_pressure": pressure, "bounded": true};
}
