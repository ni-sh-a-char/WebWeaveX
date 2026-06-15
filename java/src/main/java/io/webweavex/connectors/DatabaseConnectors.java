package io.webweavex.connectors;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * Port of {@code core.connectors.database_connector_engine.extract_database_runtime}
 * and its postgres/mysql/sqlite/redis sub-engines. Deterministic transform over a
 * caller-supplied snapshot; no live connection.
 */
public final class DatabaseConnectors {

    private DatabaseConnectors() {
    }

    /** {@code extract_database_runtime}. */
    public static Map<String, Object> extractDatabaseRuntime(
            String databaseType, Map<String, Object> snapshot) {
        String normalized = databaseType.toLowerCase(Locale.ROOT);
        try {
            switch (normalized) {
                case "postgres":
                case "postgresql":
                    return extractPostgresRuntime(snapshot);
                case "mysql":
                    return extractMysqlRuntime(snapshot);
                case "sqlite":
                    return extractSqliteRuntime(snapshot);
                case "redis":
                    return extractRedisRuntime(snapshot);
                default:
                    break;
            }
        } catch (RuntimeException e) {
            return degraded(normalized);
        }
        return degraded(normalized);
    }

    private static Map<String, Object> degraded(String databaseType) {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("database_type", databaseType);
        out.put("schemas", new ArrayList<>());
        out.put("tables", new ArrayList<>());
        out.put("metrics", new LinkedHashMap<>());
        out.put("degraded", true);
        out.put("reason", "connector_unavailable");
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_postgres_runtime}. */
    public static Map<String, Object> extractPostgresRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("database_type", "postgresql");
        out.put("schemas", Connectors.getList(s, "schemas", Connectors.list("public")));
        out.put("tables", Connectors.sortedByStr(Connectors.getList(s, "tables", new ArrayList<>())));
        out.put("indexes", Connectors.getList(s, "indexes", new ArrayList<>()));
        out.put("metrics", Connectors.getMap(s, "metrics"));
        out.put("active_connections", Connectors.pyInt(Py.get(s, "active_connections", 0L)));
        out.put("replication_state", Py.str(Py.get(s, "replication_state", "unknown")));
        out.put("degraded", Py.get(s, "degraded", false));
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_mysql_runtime}. */
    public static Map<String, Object> extractMysqlRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("database_type", "mysql");
        out.put("schemas", Connectors.getList(s, "schemas", new ArrayList<>()));
        out.put("tables", Connectors.sortedByStr(Connectors.getList(s, "tables", new ArrayList<>())));
        out.put("indexes", Connectors.getList(s, "indexes", new ArrayList<>()));
        out.put("metrics", Connectors.getMap(s, "metrics"));
        out.put("active_connections", Connectors.pyInt(Py.get(s, "active_connections", 0L)));
        out.put("replication_state", Py.str(Py.get(s, "replication_state", "")));
        out.put("degraded", Py.get(s, "degraded", false));
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_sqlite_runtime}. */
    public static Map<String, Object> extractSqliteRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("database_type", "sqlite");
        out.put("schemas", Connectors.list("main"));
        out.put("tables", Connectors.sortedByStr(Connectors.getList(s, "tables", new ArrayList<>())));
        out.put("indexes", Connectors.getList(s, "indexes", new ArrayList<>()));
        out.put("metrics", Connectors.getMap(s, "metrics"));
        out.put("active_connections", 1L);
        out.put("replication_state", "local");
        out.put("degraded", Py.get(s, "degraded", false));
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_redis_runtime}. */
    public static Map<String, Object> extractRedisRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("database_type", "redis");
        out.put("schemas", new ArrayList<>());
        out.put("tables", Connectors.slice(Connectors.getList(s, "keys", new ArrayList<>()), 1000));
        out.put("indexes", new ArrayList<>());
        out.put("metrics", Connectors.getMap(s, "metrics"));
        out.put("active_connections", Connectors.pyInt(Py.get(s, "clients", 0L)));
        out.put("replication_state", Py.str(Py.get(s, "role", "master")));
        out.put("streams", Connectors.getList(s, "streams", new ArrayList<>()));
        out.put("degraded", Py.get(s, "degraded", false));
        out.put("bounded", true);
        return out;
    }
}
