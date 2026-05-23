/** Port of core/connectors/postgres_connector_engine.py */
export function extractPostgresRuntime(
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    database_type: "postgresql",
    schemas: [...((snapshot.schemas as unknown[]) ?? ["public"])].map(String),
    tables: [...((snapshot.tables as unknown[]) ?? [])].map(String).sort(),
    indexes: [...((snapshot.indexes as unknown[]) ?? [])],
    metrics: { ...((snapshot.metrics as Record<string, unknown>) ?? {}) },
    active_connections: Number(snapshot.active_connections ?? 0),
    replication_state: String(snapshot.replication_state ?? "unknown"),
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
