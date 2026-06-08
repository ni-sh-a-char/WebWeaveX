/**
 * Converted from Python: core/universal/universal_router_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function routeInput(source: any): any {
  var s: any = String(py.or2(source, () => (""))).toLowerCase();
  if (py.truthy(py.startswith(s, "http"))) {
    return "web";
  }
  if (py.truthy(py.endswith(s, ".pdf"))) {
    return "pdf";
  }
  if (py.truthy(py.endswith(s, ".json"))) {
    return "json";
  }
  return "text";
}
