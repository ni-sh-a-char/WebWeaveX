export function extractMysqlRuntime(snapshot: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    database_type: "mysql",
    schemas: [...((snapshot.schemas as unknown[]) ?? [])],
    tables: [...((snapshot.tables as unknown[]) ?? [])].map(String).sort(),
    indexes: [...((snapshot.indexes as unknown[]) ?? [])],
    metrics: { ...(snapshot.metrics as Record<string, unknown>) },
    active_connections: Number(snapshot.active_connections ?? 0),
    replication_state: String(snapshot.replication_state ?? ""),
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
