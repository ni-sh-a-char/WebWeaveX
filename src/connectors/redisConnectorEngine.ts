/**
 * Converted from Python: core/connectors/redis_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractRedisRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"database_type": "redis", "schemas": [], "tables": py.slice([...py.iter(py.get(snap, "keys", []))], null, 1000), "indexes": [], "metrics": py.pyDict(py.get(snap, "metrics", {})), "active_connections": py.toInt(py.get(snap, "clients", 0)), "replication_state": py.toStr(py.get(snap, "role", "master")), "streams": [...py.iter(py.get(snap, "streams", []))], "degraded": py.get(snap, "degraded", false), "bounded": true};
}
