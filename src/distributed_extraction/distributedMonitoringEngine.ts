/**
 * Converted from Python: core/distributed_extraction/distributed_monitoring_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function monitorExtractionCluster(workers: any, queue: any): any {
  var statuses: Record<string, any> = {};
  var worker: any;
  for (worker of py.iter(workers)) {
    var status: any = py.toStr(py.get(worker, "status", "unknown"));
    py.setItem(statuses, status, py.add(py.get(statuses, status, 0), 1));
  }
  return {"worker_statuses": py.pyDict(py.sorted(py.items(statuses))), "queue_depth": py.len(queue), "active_workers": py.add(py.get(statuses, "idle", 0), py.get(statuses, "running", 0)), "bounded": true};
}
