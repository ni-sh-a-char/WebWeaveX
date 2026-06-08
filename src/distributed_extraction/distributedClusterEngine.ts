/**
 * Converted from Python: core/distributed_extraction/distributed_cluster_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildClusterState(workers: any, queue: any): any {
  return {"worker_count": py.len(workers), "queue_depth": py.len(queue), "worker_ids": py.sorted(py.iter(workers).map((worker: any) => py.toStr(py.get(worker, "worker_id", "")))), "bounded": true};
}
