export function buildClusterState(
  workers: Record<string, unknown>[],
  queue: Record<string, unknown>[],
): Record<string, unknown> {
  return {
    worker_count: workers.length,
    queue_depth: queue.length,
    worker_ids: workers.map((w) => String(w.worker_id ?? "")).sort(),
    bounded: true,
  };
}
