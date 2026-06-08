/**
 * Converted from Python: core/distributed_extraction/distributed_failover_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { balanceExtractionWorkloads } from "./distributedLoadBalancer.js";
import { recoverDistributedRuntime } from "./distributedRecoveryEngine.js";
import { createExtractionWorker } from "./extractionWorkerEngine.js";

export function failoverExtractionRuntime(checkpoint: any, dead_worker_id: any): any {
  var workers: any = [...py.iter(py.get(checkpoint, "workers", []))];
  var tasks: any = [...py.iter(py.get(checkpoint, "queue", []))];
  var surviving: any = py.iter(workers).filter((worker: any) => !py.eq(py.toStr(py.get(worker, "worker_id", "")), dead_worker_id)).map((worker: any) => worker);
  var replacement: any = createExtractionWorker(`${py.toStr(dead_worker_id)}_migrated`, {}, {}, {}, {}, "migrated");
  py.listAppend(surviving, replacement);
  var recovered: any = py.callKw(recoverDistributedRuntime as (...a: any[]) => any, ["checkpoint"], {"checkpoint": checkpoint, "failed_worker_ids": [dead_worker_id]});
  var assignments: any = balanceExtractionWorkloads(surviving, tasks);
  return {"dead_worker": dead_worker_id, "replacement_worker": py.at(replacement, "worker_id"), "assignments": py.get(assignments, "assignments", []), "recovered": recovered, "bounded": true};
}
export { balanceExtractionWorkloads, createExtractionWorker, recoverDistributedRuntime };
