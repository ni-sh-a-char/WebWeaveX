/**
 * Converted from Python: core/connectors/sqlite_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractSqliteRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"database_type": "sqlite", "schemas": ["main"], "tables": py.sorted(py.get(snap, "tables", []), {key: (py.toStr) as (item: any) => any}), "indexes": [...py.iter(py.get(snap, "indexes", []))], "metrics": py.pyDict(py.get(snap, "metrics", {})), "active_connections": 1, "replication_state": "local", "degraded": py.get(snap, "degraded", false), "bounded": true};
}
