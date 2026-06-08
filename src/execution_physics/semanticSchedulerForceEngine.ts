/**
 * Converted from Python: core/execution_physics/semantic_scheduler_force_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_FORCE: any = 100000;
export function computeSchedulerForce(runtime_ir: any): any {
  var tasks: any = py.len([...py.iter(py.or2(py.get(runtime_ir, "tasks", []), () => ([])))]);
  var workers: any = py.max([py.len([...py.iter(py.or2(py.get(runtime_ir, "distributed_workers", []), () => ([])))]), 1]);
  var force: any = py.min([py.mul(tasks, workers), MAX_FORCE]);
  return {"scheduler_force": force, "task_count": tasks, "bounded": true};
}
