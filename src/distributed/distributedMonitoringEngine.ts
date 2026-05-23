export function monitorExtractionCluster(
  workers: Record<string, unknown>[],
  queue: Record<string, unknown>[],
): Record<string, unknown> {
  return {
    workers_online: workers.filter((w) => w.status !== "offline").length,
    queue_depth: queue.length,
    healthy: workers.length > 0,
    bounded: true,
  };
}
