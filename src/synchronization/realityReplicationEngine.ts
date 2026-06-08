/**
 * Converted from Python: core/synchronization/reality_replication_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function replicateRuntimeReality(source: any, workers: any): any {
  var replicas: any[] = [];
  var index: any;
  var worker: any;
  for ([index, worker] of py.enumerate(py.slice(workers, null, 1000))) {
    py.listAppend(replicas, {"worker_id": py.toStr(py.get(worker, "worker_id", py.get(worker, "id", `worker:${py.toStr(index)}`))), "reality_id": py.toStr(py.get(source, "reality_id", "primary")), "semantic_state": py.pyDict(py.get(source, "semantic_state", {})), "runtime_state": py.pyDict(py.get(source, "runtime_state", {})), "workflows": py.pyDict(py.get(source, "workflows", {})), "checkpoints": [...py.iter(py.get(source, "checkpoints", []))], "causality_graph": py.pyDict(py.get(source, "causality_graph", {})), "replicated": true});
  }
  return {"replicas": replicas, "replica_count": py.len(replicas), "bounded": true};
}
