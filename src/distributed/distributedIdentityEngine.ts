export function routeBrowserIdentity(workers: Record<string, unknown>[]): Record<string, unknown> {
  const routes = workers.map((worker) => ({
    worker_id: String(worker.worker_id ?? ""),
    identity_hash: String(
      (worker.identity as Record<string, unknown>)?.fingerprint_hash ??
        (worker.identity as Record<string, unknown>)?.runtime_identity ??
        worker.worker_id,
    ),
    bounded: true,
  }));
  routes.sort((a, b) => String(a.worker_id).localeCompare(String(b.worker_id)));
  return { routes, bounded: true };
}
