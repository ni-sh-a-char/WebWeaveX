/**
 * Converted from Python: core/runtime/distributed_worker_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_WORKERS: any = 128;
export function assignDistributedWorkers(tasks: any): any {
  var assignments: any[] = [];
  var worker_id: any = 0;
  var task: any;
  for (task of py.iter(tasks)) {
    py.listAppend(assignments, {"worker": worker_id, "task": task});
    worker_id = py.mod(py.add(worker_id, 1), MAX_WORKERS);
  }
  return {"assignments": assignments, "workers_used": py.min([py.len(tasks), MAX_WORKERS])};
}
