import { extractMysqlRuntime } from "./mysqlConnector.js";
import { extractPostgresRuntime } from "./postgresConnector.js";
import { extractRedisRuntime } from "./redisConnector.js";
import { extractSqliteRuntime } from "./sqliteConnector.js";

export function extractDatabaseRuntime(
  databaseType = "postgresql",
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  const n = databaseType.toLowerCase();
  if (n === "postgres" || n === "postgresql") return extractPostgresRuntime(snapshot);
  if (n === "mysql") return extractMysqlRuntime(snapshot);
  if (n === "sqlite") return extractSqliteRuntime(snapshot);
  if (n === "redis") return extractRedisRuntime(snapshot);
  return { database_type: n, degraded: true, bounded: true };
}
