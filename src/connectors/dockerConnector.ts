export function extractDockerRuntime(snapshot: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    runtime: "docker",
    containers: [...((snapshot.containers as unknown[]) ?? [])],
    images: [...((snapshot.images as unknown[]) ?? [])].map(String).sort(),
    volumes: [...((snapshot.volumes as unknown[]) ?? [])],
    networks: [...((snapshot.networks as unknown[]) ?? [])],
    states: { ...(snapshot.states as Record<string, unknown>) },
    health: { ...(snapshot.health as Record<string, unknown>) },
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
