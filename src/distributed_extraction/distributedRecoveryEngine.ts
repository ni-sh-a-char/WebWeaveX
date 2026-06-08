/**
 * Converted from Python: core/distributed_extraction/distributed_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { createExtractionWorker } from "./extractionWorkerEngine.js";

export function recoverDistributedRuntime(checkpoint: any, failed_worker_ids: any = null): any {
  var failed: any = py.toSet(py.or2(failed_worker_ids, () => ([])));
  var workers: any = [...py.iter(py.get(checkpoint, "workers", []))];
  var queue: any = [...py.iter(py.get(checkpoint, "queue", []))];
  var recovered_workers: any[] = [];
  var worker: any;
  for (worker of py.iter(workers)) {
    var worker_id: any = py.toStr(py.get(worker, "worker_id", ""));
    if (py.contains(failed, worker_id)) {
      py.listAppend(recovered_workers, createExtractionWorker(worker_id, py.get(worker, "runtime_state", {}), py.get(worker, "identity", {}), py.get(worker, "adaptive_runtime", {}), py.get(worker, "stream_runtime", {}), "recovered"));
    } else {
      py.listAppend(recovered_workers, worker);
    }
  }
  return {"workers": recovered_workers, "queue": queue, "runtime_graph": py.get(checkpoint, "runtime_graph", {}), "stream_runtime": py.get(checkpoint, "stream_runtime", {}), "adaptive_memory": py.get(checkpoint, "adaptive_memory", {}), "recovered": true, "bounded": true};
}
export { createExtractionWorker };
