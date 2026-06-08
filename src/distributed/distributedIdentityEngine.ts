export function routeBrowserIdentity(workers: Record<string, unknown>[]): Record<string, unknown> {
  const routes = workers.map((worker) => {
    const identity = (worker.identity as Record<string, unknown>) ?? {};
    return {
      worker_id: String(worker.worker_id ?? ""),
      profile_id: String(identity.profile_id ?? "default"),
      fingerprint_hash: String(identity.fingerprint_hash ?? identity.runtime_identity ?? worker.worker_id ?? ""),
    };
  });
  routes.sort((a, b) => String(a.worker_id).localeCompare(String(b.worker_id)));
  return { routes, bounded: true };
}
