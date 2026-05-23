/** Port of core/connectors/kubernetes_connector_engine.py */
export function extractKubernetesRuntime(
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  const pods = [...((snapshot.pods as Record<string, unknown>[]) ?? [])].sort((a, b) =>
    String(a.name ?? a).localeCompare(String(b.name ?? b)),
  );
  const deployments = [...((snapshot.deployments as Record<string, unknown>[]) ?? [])].sort(
    (a, b) => String(a.name ?? a).localeCompare(String(b.name ?? b)),
  );
  return {
    namespaces: [...((snapshot.namespaces as unknown[]) ?? ["default"])].map(String).sort(),
    pods,
    deployments,
    services: [...((snapshot.services as unknown[]) ?? [])],
    ingress: [...((snapshot.ingress as unknown[]) ?? [])],
    topology: { ...((snapshot.topology as Record<string, unknown>) ?? {}) },
    events: [...((snapshot.events as unknown[]) ?? [])].slice(0, 5000),
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
