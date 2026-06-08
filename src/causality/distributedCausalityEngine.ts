/**
 * Converted from Python: core/causality/distributed_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDistributedCausality(distributed_result: any = null, worker_events: any = null): any {
  distributed_result = py.or2(distributed_result, () => ({}));
  worker_events = [...py.iter(py.or2(worker_events, () => ([])))];
  var workers: any = [...py.iter(py.get(distributed_result, "workers", []))];
  var chains: any[] = [];
  var index: any;
  var event: any;
  for ([index, event] of py.enumerate(py.slice(worker_events, null, 10000))) {
    py.listAppend(chains, {"worker_id": py.toStr(py.get(event, "worker_id", `worker_${py.toStr(index)}`)), "event_id": py.toStr(py.get(event, "id", `dist:${py.toStr(index)}`)), "step": index, "relation": "cluster_sync"});
  }
  return {"worker_causality": chains, "autonomous_propagation": py.get(distributed_result, "autonomous", false), "remote_chains": py.slice([...py.iter(py.get(distributed_result, "tasks", []))], null, 1000), "cluster_synchronization": {"worker_count": py.len(workers), "synced": py.truthy(workers)}, "bounded": true};
}
