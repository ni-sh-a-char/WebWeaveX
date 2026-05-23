/** Port of core/connectors/redis_connector_engine.py */
export function extractRedisRuntime(
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  const keys = [...((snapshot.keys as unknown[]) ?? [])].slice(0, 1000);
  return {
    database_type: "redis",
    schemas: [],
    tables: keys,
    indexes: [],
    metrics: { ...((snapshot.metrics as Record<string, unknown>) ?? {}) },
    active_connections: Number(snapshot.clients ?? 0),
    replication_state: String(snapshot.role ?? "master"),
    streams: [...((snapshot.streams as unknown[]) ?? [])],
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
