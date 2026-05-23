export function extractCicdRuntime(
  provider = "github_actions",
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    provider,
    workflows: [...((snapshot.workflows as unknown[]) ?? [])],
    jobs: [...((snapshot.jobs as unknown[]) ?? [])],
    logs: [...((snapshot.logs as unknown[]) ?? [])].slice(0, 1000),
    artifacts: [...((snapshot.artifacts as unknown[]) ?? [])],
    failures: [...((snapshot.failures as unknown[]) ?? [])],
    deployment_graph: { ...(snapshot.deployment_graph as Record<string, unknown>) },
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
