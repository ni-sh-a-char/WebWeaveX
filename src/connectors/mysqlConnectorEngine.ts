/**
 * Converted from Python: core/connectors/mysql_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractMysqlRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"database_type": "mysql", "schemas": [...py.iter(py.get(snap, "schemas", []))], "tables": py.sorted(py.get(snap, "tables", []), {key: (py.toStr) as (item: any) => any}), "indexes": [...py.iter(py.get(snap, "indexes", []))], "metrics": py.pyDict(py.get(snap, "metrics", {})), "active_connections": py.toInt(py.get(snap, "active_connections", 0)), "replication_state": py.toStr(py.get(snap, "replication_state", "")), "degraded": py.get(snap, "degraded", false), "bounded": true};
}
