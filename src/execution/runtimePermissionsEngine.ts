/**
 * Converted from Python: core/execution/runtime_permissions_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _SCOPES: any = ["browser", "native", "filesystem", "connector", "terminal", "vm"];
export function buildRuntimePermissions(scopes: any = null): any {
  var active: any = py.sorted(py.toSet(py.or2(scopes, () => (["browser", "native"]))));
  return {"scopes": Object.fromEntries(py.iter(_SCOPES).map((scope: any) => ([scope, py.contains(active, scope)] as [any, any]))), "active_scopes": active, "bounded": true};
}
export function validateRuntimePermissions(permissions: any, runtime: any, action_type: any): any {
  var scopes: any = py.get(permissions, "scopes", {});
  var runtime_scope: any = (py.contains(_SCOPES, runtime) ? runtime : "browser");
  if ((py.truthy(py.startswith(action_type, "terminal_")) || py.eq(action_type, "terminal_command"))) {
    runtime_scope = "terminal";
  } else if (py.truthy(py.startswith(action_type, "native_"))) {
    runtime_scope = "native";
  } else if (py.truthy(py.startswith(action_type, "vm_"))) {
    runtime_scope = "vm";
  } else if (py.truthy(py.startswith(action_type, "connector_"))) {
    runtime_scope = "connector";
  }
  var allowed: any = py.truthy(py.get(scopes, runtime_scope, false));
  return {"allowed": allowed, "scope": runtime_scope, "deterministic": true, "bounded": true};
}
