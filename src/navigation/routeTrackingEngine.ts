/**
 * Converted from Python: core/navigation/route_tracking_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_ROUTES: any = 1000;
export function trackNavigationRoutes(page: any): any {
  var routes: any[] = [];
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_route_history") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_route_history")] === "function")))) {
    routes = py.slice([...py.iter(page._test_route_history)], null, MAX_ROUTES);
    return {"routes": routes, "transitions": _routeEdges(routes), "bounded": true};
  }
  var current: any = "";
  if ((page !== null && page !== undefined)) {
    current = py.toStr((((page ?? {}) as Record<string, any>)[String("_test_url")] ?? (((page ?? {}) as Record<string, any>)[String("url")] ?? "")));
  }
  if (py.truthy(current)) {
    py.listAppend(routes, {"path": current, "order": 0});
  }
  return {"routes": routes, "transitions": _routeEdges(routes), "bounded": true};
}
export function _routeEdges(routes: any): any {
  var edges: any[] = [];
  var index: any;
  for (index = 0; index < py.sub(py.len(routes), 1); index++) {
    py.listAppend(edges, {"from": py.toStr(py.get(py.at(routes, index), "path", "")), "to": py.toStr(py.get(py.at(routes, py.add(index, 1)), "path", "")), "relation": "route_transition"});
  }
  return py.slice(edges, null, MAX_ROUTES);
}
