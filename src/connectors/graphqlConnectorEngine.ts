/**
 * Converted from Python: core/connectors/graphql_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractGraphqlRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"protocol": "graphql", "endpoints": [...py.iter(py.get(snap, "endpoints", ["/graphql"]))], "schemas": [...py.iter(py.get(snap, "schemas", []))], "types": py.sorted(py.get(snap, "types", []), {key: (py.toStr) as (item: any) => any}), "bounded": true};
}
