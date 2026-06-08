/**
 * Converted from Python: core/repository/recursive/service_discovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function discoverServices(topology: any, routes: any): any {
  var services: any = py.sorted(py.toSet(py.get(topology, "services", [])));
  var apis: any = py.sorted(py.toSet(py.get(routes, "routes", [])));
  return {"services": services, "apis": apis, "workers": [], "schedulers": [], "queues": [], "gateways": []};
}
