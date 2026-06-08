/**
 * Converted from Python: core/runtime_language/wwx_validator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _ALLOWED: any = py.toSet(new Set(["EXTRACT", "SYNC", "REPLAY", "EXECUTE", "FEDERATE", "RECONSTRUCT", "MEMORY"]));
export function validateWwx(parsed: any): any {
  var errors: any[] = [];
  var stmt: any;
  for (stmt of py.iter(py.get(parsed, "statements", []))) {
    if (!py.contains(_ALLOWED, py.get(stmt, "verb"))) {
      py.listAppend(errors, `forbidden verb: ${py.toStr(py.get(stmt, "verb"))}`);
    }
  }
  return {"valid": !py.truthy(errors), "errors": py.sorted(errors), "bounded": true};
}
