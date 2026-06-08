/**
 * Converted from Python: core/distributed_extraction/distributed_load_balancer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_WORKERS: any = 1000;
export function balanceExtractionWorkloads(workers: any, tasks: any): any {
  var assignments: any[] = [];
  if (!py.truthy(workers)) {
    return {"assignments": [], "bounded": true};
  }
  var active_workers: any = py.sorted(py.slice(workers, null, MAX_WORKERS), {key: ((item: any) => py.toStr(py.get(item, "worker_id", ""))) as (item: any) => any});
  var index: any;
  var task: any;
  for ([index, task] of py.enumerate(tasks)) {
    var worker: any = py.at(active_workers, py.mod(index, py.len(active_workers)));
    py.listAppend(assignments, {"task_id": py.toStr(py.get(task, "task_id", `task_${py.toStr(index)}`)), "worker_id": py.toStr(py.get(worker, "worker_id", "")), "partition": py.mod(index, py.len(active_workers))});
  }
  return {"assignments": py.sorted(assignments, {key: ((item: any) => [py.toStr(py.get(item, "worker_id", "")), py.toStr(py.get(item, "task_id", ""))]) as (item: any) => any}), "bounded": true};
}
