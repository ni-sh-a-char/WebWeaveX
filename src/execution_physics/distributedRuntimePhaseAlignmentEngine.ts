/**
 * Converted from Python: core/execution_physics/distributed_runtime_phase_alignment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function alignRuntimePhases(runtime_ir: any): any {
  var workers: any = py.len([...py.iter(py.or2(py.get(runtime_ir, "distributed_workers", []), () => ([])))]);
  var tasks: any = py.len([...py.iter(py.or2(py.get(runtime_ir, "tasks", []), () => ([])))]);
  var aligned: any = py.or2(py.eq(workers, 0), () => (py.le(tasks, workers)));
  return {"phase_aligned": aligned, "worker_count": workers, "task_count": tasks};
}
