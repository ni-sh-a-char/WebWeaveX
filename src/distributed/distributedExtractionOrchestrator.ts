import { synchronizeAdaptiveRuntime } from "./distributedAdaptiveRuntimeEngine.js";
import { buildClusterState } from "./distributedClusterEngine.js";
import { routeBrowserIdentity } from "./distributedIdentityEngine.js";
import { monitorExtractionCluster } from "./distributedMonitoringEngine.js";
import { buildDistributedRuntimeGraph } from "./distributedRuntimeGraphEngine.js";
import { routeAuthenticatedSessions } from "./distributedSessionEngine.js";
import { federateStreamRuntimes } from "./distributedStreamEngine.js";
import { balanceExtractionWorkloads } from "./distributedLoadBalancer.js";
import { dequeueExtraction, enqueueExtraction } from "./extractionQueueEngine.js";
import { scheduleExtractionRuntime } from "./extractionSchedulerEngine.js";
import { createExtractionWorker } from "./extractionWorkerEngine.js";
import { federateExtractionRuntimes } from "./runtimeFederationEngine.js";

export function runDistributedExtraction(
  tasks: Record<string, unknown>[],
  workers?: Record<string, unknown>[],
  checkpoint: Record<string, unknown> = {},
  tick = 0,
  runtimeGraphs: Record<string, unknown>[] = [],
): Record<string, unknown> {
  let queue = [...((checkpoint.queue as Record<string, unknown>[]) ?? [])];
  let workerList = [...(workers ?? (checkpoint.workers as Record<string, unknown>[]) ?? [])];

  if (!workerList.length) {
    workerList = [
      createExtractionWorker("worker_0", {}, { profile_id: "default", fingerprint_hash: "fp0" }, {
        memory: { healed_selectors: {} },
      }, { events: [] }),
    ];
  }

  for (const task of tasks) {
    queue = enqueueExtraction(queue, task).queue;
  }

  const schedule = scheduleExtractionRuntime(tasks, tick);
  const assignments = balanceExtractionWorkloads(workerList, tasks);
  const sessionRoutes = routeAuthenticatedSessions(workerList);
  const identityRoutes = routeBrowserIdentity(workerList);
  const adaptiveSync = synchronizeAdaptiveRuntime(
    workerList.map((w) => (w.adaptive_runtime as Record<string, unknown>) ?? {}),
  );
  const streamFederation = federateStreamRuntimes(
    workerList.map((w) => ({
      worker_id: w.worker_id,
      events: ((w.stream_runtime as Record<string, unknown>)?.events as unknown[]) ?? [],
    })),
  );
  const federation = federateExtractionRuntimes(runtimeGraphs);
  const distributedGraph = buildDistributedRuntimeGraph(
    workerList,
    federation.topology as Record<string, unknown>,
  );
  const monitoring = monitorExtractionCluster(workerList, queue);
  const cluster = buildClusterState(workerList, queue);

  const nextCheckpoint = {
    queue,
    workers: workerList,
    runtime_graph: distributedGraph,
    identities: identityRoutes.routes as unknown[],
    adaptive_memory: adaptiveSync,
    stream_runtime: streamFederation,
    tick: tick + 1,
    assignments: assignments.assignments as unknown[],
    bounded: true,
  };

  return {
    workers: workerList,
    queue,
    schedule,
    assignments,
    session_routes: sessionRoutes,
    identity_routes: identityRoutes,
    adaptive_sync: adaptiveSync,
    stream_federation: streamFederation,
    topology: federation,
    distributed_graph: distributedGraph,
    monitoring,
    cluster,
    checkpoint: nextCheckpoint,
    bounded: true,
  };
}

export { dequeueExtraction, enqueueExtraction, createExtractionWorker };
