/**
 * Converted from Python: core/repository/semantic/semantic_api_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function reconstructSemanticApi(text: any): any {
  var source: any = py.or2(text, () => (""));
  var routes: Set<any> = new Set();
  var methods: Set<any> = new Set();
  var handlers: Set<any> = new Set();
  var m: any;
  for (m of py.iter(py.reFinditer("@(app|router)\\.(get|post|put|delete|patch)\\(['\\\"]([^'\\\"]+)['\\\"]", source, ""))) {
    py.setAdd(methods, String(m.group(2)).toUpperCase());
    py.setAdd(routes, m.group(3));
  }
  for (m of py.iter(py.reFinditer("\\b(app|router)\\.(get|post|put|delete|patch)\\(['\\\"]([^'\\\"]+)['\\\"]\\s*,\\s*([A-Za-z_][A-Za-z0-9_]*)", source, ""))) {
    py.setAdd(methods, String(m.group(2)).toUpperCase());
    py.setAdd(routes, m.group(3));
    py.setAdd(handlers, m.group(4));
  }
  for (m of py.iter(py.reFinditer("\\b(function|def|fun)\\s+([A-Za-z_][A-Za-z0-9_]*)", source, ""))) {
    py.setAdd(handlers, m.group(2));
  }
  return {"routes": py.sorted(routes), "methods": py.sorted(methods), "handlers": py.sorted(handlers)};
}
