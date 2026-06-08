/**
 * Converted from Python: core/connectors/database_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractMysqlRuntime } from "./mysqlConnectorEngine.js";
import { extractPostgresRuntime } from "./postgresConnectorEngine.js";
import { extractRedisRuntime } from "./redisConnectorEngine.js";
import { extractSqliteRuntime } from "./sqliteConnectorEngine.js";

export function extractDatabaseRuntime(database_type: any = "postgresql", snapshot: any = null): any {
  var normalized: any = String(database_type).toLowerCase();
  try {
    if (py.contains(["postgres", "postgresql"], normalized)) {
      return extractPostgresRuntime(snapshot);
    }
    if (py.eq(normalized, "mysql")) {
      return extractMysqlRuntime(snapshot);
    }
    if (py.eq(normalized, "sqlite")) {
      return extractSqliteRuntime(snapshot);
    }
    if (py.eq(normalized, "redis")) {
      return extractRedisRuntime(snapshot);
    }
  } catch (_e: any) {
    return _degradedDatabase(normalized);
  }
  return _degradedDatabase(normalized);
}
export function _degradedDatabase(database_type: any): any {
  return {"database_type": database_type, "schemas": [], "tables": [], "metrics": {}, "degraded": true, "reason": "connector_unavailable", "bounded": true};
}
export { extractMysqlRuntime, extractPostgresRuntime, extractRedisRuntime, extractSqliteRuntime };
