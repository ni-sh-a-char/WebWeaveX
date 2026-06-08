/**
 * Converted from Python: core/connectors/grpc_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractGrpcRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"protocol": "grpc", "services": py.sorted(py.get(snap, "services", []), {key: (py.toStr) as (item: any) => any}), "methods": py.sorted(py.get(snap, "methods", []), {key: (py.toStr) as (item: any) => any}), "schemas": [...py.iter(py.get(snap, "protobuf", []))], "bounded": true};
}
