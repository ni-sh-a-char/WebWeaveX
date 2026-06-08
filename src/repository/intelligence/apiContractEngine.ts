/**
 * Converted from Python: core/repository/intelligence/api_contract_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractApiContract(api_surface: any): any {
  var routes: any = py.sorted(py.toSet(py.get(api_surface, "routes", [])));
  var methods: any = py.sorted(py.toSet(py.get(api_surface, "methods", [])));
  var handlers: any = py.sorted(py.toSet(py.get(api_surface, "handlers", [])));
  return {"routes": routes, "methods": methods, "handlers": handlers};
}
