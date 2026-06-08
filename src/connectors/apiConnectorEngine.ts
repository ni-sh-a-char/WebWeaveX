/**
 * Converted from Python: core/connectors/api_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractGraphqlRuntime } from "./graphqlConnectorEngine.js";
import { extractGrpcRuntime } from "./grpcConnectorEngine.js";

export function extractApiRuntime(api_type: any = "rest", snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  var normalized: any = String(api_type).toLowerCase();
  var base: any = {"api_type": normalized, "endpoints": py.sorted(py.get(snap, "endpoints", []), {key: (py.toStr) as (item: any) => any}), "schemas": [...py.iter(py.get(snap, "schemas", []))], "auth_state": py.pyDict(py.get(snap, "auth", {})), "rate_limits": py.pyDict(py.get(snap, "rate_limits", {})), "response_topology": [...py.iter(py.get(snap, "responses", []))], "pagination_models": [...py.iter(py.get(snap, "pagination", []))], "bounded": true};
  if (py.eq(normalized, "graphql")) {
    py.setItem(base, "graphql", extractGraphqlRuntime(py.get(snap, "graphql")));
  } else if (py.eq(normalized, "grpc")) {
    py.setItem(base, "grpc", extractGrpcRuntime(py.get(snap, "grpc")));
  }
  return base;
}
export { extractGraphqlRuntime, extractGrpcRuntime };
