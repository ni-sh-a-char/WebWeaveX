export function monitorExtractionCluster(
  workers: Record<string, unknown>[],
  queue: Record<string, unknown>[],
): Record<string, unknown> {
  const workerStatuses: Record<string, number> = {};
  for (const w of workers) {
    const status = String(w.status ?? "idle");
    workerStatuses[status] = (workerStatuses[status] ?? 0) + 1;
  }
  const active = workers.filter((w) => {
    const status = String(w.status ?? "idle");
    return status === "idle" || status === "running" || status === "busy";
  }).length;
  return {
    worker_statuses: workerStatuses,
    queue_depth: queue.length,
    active_workers: active,
    bounded: true,
  };
}
