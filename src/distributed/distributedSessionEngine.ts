export function routeAuthenticatedSessions(workers: Record<string, unknown>[]): Record<string, unknown> {
  const routes = workers.map((worker) => {
    const workerId = String(worker.worker_id ?? "");
    const session = ((worker.runtime_state as Record<string, unknown>)?.session ?? {}) as Record<
      string,
      unknown
    >;
    return {
      worker_id: workerId,
      session_fingerprint: String(session.session_fingerprint ?? workerId),
      isolated: true,
    };
  });
  routes.sort((a, b) => String(a.worker_id).localeCompare(String(b.worker_id)));
  return { routes, bounded: true };
}
