/**
 * Converted from Python: core/runtime/semantic_security_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function validateSemanticBoundary(payload: any): any {
  var blocked: any = py.any(py.keys(payload).map((key: any) => py.startswith(String(key).toLowerCase(), "__")));
  return {"accepted": !py.truthy(blocked), "blocked": blocked};
}
