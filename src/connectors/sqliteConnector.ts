export function extractSqliteRuntime(snapshot: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    database_type: "sqlite",
    schemas: ["main"],
    tables: [...((snapshot.tables as unknown[]) ?? [])].map(String).sort(),
    indexes: [...((snapshot.indexes as unknown[]) ?? [])],
    metrics: { ...(snapshot.metrics as Record<string, unknown>) },
    active_connections: 1,
    replication_state: "local",
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
