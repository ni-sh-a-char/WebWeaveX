/**
 * Converted from Python: core/distributed_extraction/distributed_extraction_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { synchronizeAdaptiveRuntime } from "./distributedAdaptiveRuntimeEngine.js";
import { buildClusterState } from "./distributedClusterEngine.js";
import { routeBrowserIdentity } from "./distributedIdentityEngine.js";
import { monitorExtractionCluster } from "./distributedMonitoringEngine.js";
import { recoverDistributedRuntime } from "./distributedRecoveryEngine.js";
import { buildDistributedRuntimeGraph } from "./distributedRuntimeGraphEngine.js";
import { routeAuthenticatedSessions } from "./distributedSessionEngine.js";
import { federateStreamRuntimes } from "./distributedStreamEngine.js";
import { dequeueExtraction, enqueueExtraction } from "./extractionQueueEngine.js";
import { scheduleExtractionRuntime } from "./extractionSchedulerEngine.js";
import { createExtractionWorker } from "./extractionWorkerEngine.js";
import { federateExtractionRuntimes } from "./runtimeFederationEngine.js";
import { balanceExtractionWorkloads } from "./distributedLoadBalancer.js";

export function runDistributedExtraction(tasks: any, workers: any = null, checkpoint: any = null, tick: any = 0, runtime_graphs: any = null): any {
  checkpoint = py.pyDict(py.or2(checkpoint, () => ({})));
  var queue: any = [...py.iter(py.get(checkpoint, "queue", []))];
  var worker_list: any = [...py.iter(py.or2(workers, () => (py.get(checkpoint, "workers", []))))];
  if (!py.truthy(worker_list)) {
    worker_list = [createExtractionWorker("worker_0", undefined, {"profile_id": "default", "fingerprint_hash": "fp0"}, {"memory": {"healed_selectors": {}}}, {"events": []})];
  }
  var task: any;
  for (task of py.iter(tasks)) {
    var queued: any = enqueueExtraction(queue, task);
    queue = py.at(queued, "queue");
  }
  var schedule: any = scheduleExtractionRuntime(tasks, tick);
  var assignments: any = balanceExtractionWorkloads(worker_list, tasks);
  var session_routes: any = routeAuthenticatedSessions(worker_list);
  var identity_routes: any = routeBrowserIdentity(worker_list);
  var adaptive_sync: any = synchronizeAdaptiveRuntime(py.iter(worker_list).map((worker: any) => py.get(worker, "adaptive_runtime", {})));
  var stream_federation: any = federateStreamRuntimes(py.iter(worker_list).map((worker: any) => ({"worker_id": py.get(worker, "worker_id"), "events": py.get(py.get(worker, "stream_runtime", {}), "events", [])})));
  var federation: any = federateExtractionRuntimes(py.or2(runtime_graphs, () => ([])));
  var distributed_graph: any = buildDistributedRuntimeGraph(worker_list, py.get(federation, "topology", {}));
  var monitoring: any = monitorExtractionCluster(worker_list, queue);
  var cluster: any = buildClusterState(worker_list, queue);
  var next_checkpoint: any = {"queue": queue, "workers": worker_list, "runtime_graph": distributed_graph, "identities": py.get(identity_routes, "routes", []), "adaptive_memory": adaptive_sync, "stream_runtime": stream_federation, "tick": py.add(tick, 1), "assignments": py.get(assignments, "assignments", []), "bounded": true};
  return {"workers": worker_list, "queue": queue, "schedule": schedule, "assignments": assignments, "session_routes": session_routes, "identity_routes": identity_routes, "adaptive_sync": adaptive_sync, "stream_federation": stream_federation, "topology": federation, "distributed_graph": distributed_graph, "monitoring": monitoring, "cluster": cluster, "checkpoint": next_checkpoint, "bounded": true};
}
export { balanceExtractionWorkloads, buildClusterState, buildDistributedRuntimeGraph, createExtractionWorker, dequeueExtraction, enqueueExtraction, federateExtractionRuntimes, federateStreamRuntimes, monitorExtractionCluster, recoverDistributedRuntime, routeAuthenticatedSessions, routeBrowserIdentity, scheduleExtractionRuntime, synchronizeAdaptiveRuntime };
