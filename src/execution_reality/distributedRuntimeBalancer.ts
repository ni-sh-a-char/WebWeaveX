/**
 * Converted from Python: core/execution_reality/distributed_runtime_balancer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function balanceRuntimeLoad(runtime_ir: any): any {
  var workers_raw: any = py.get(runtime_ir, "distributed_workers", []);
  if (((workers_raw !== null && typeof workers_raw === "object" && !Array.isArray(workers_raw) && !(workers_raw instanceof Set) && !(workers_raw instanceof Map)))) {
    var workers: any = [...py.iter(py.get(workers_raw, "assignments", []))];
  } else {
    workers = [...py.iter(workers_raw)];
  }
  var assignments: Record<string, any> = {};
  var idx: any;
  var worker: any;
  for ([idx, worker] of py.enumerate(workers)) {
    if (((worker !== null && typeof worker === "object" && !Array.isArray(worker) && !(worker instanceof Set) && !(worker instanceof Map)))) {
      var worker_id: any = py.toStr(py.or2(py.get(worker, "worker"), () => (py.or2(py.get(worker, "id"), () => (idx)))));
    } else {
      worker_id = py.toStr(worker);
    }
    py.setItem(assignments, worker_id, idx);
  }
  return {"assignments": py.pyDict(py.sorted(py.items(assignments)))};
}
