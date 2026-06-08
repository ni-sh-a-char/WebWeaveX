/**
 * Converted from Python: core/repository/semantic/semantic_service_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function inferSemanticServices(topology: any, imports: any, routes: any, dependencies: any): any {
  var modules: any = py.sorted(py.toSet(py.get(py.or2(topology, () => ({})), "modules", [])));
  var services: any = py.sorted(py.toSet(py.iter(modules).filter((m: any) => (py.contains(m, "/") || py.contains(m, "\\"))).map((m: any) => m)));
  var apis: any = py.sorted(py.toSet(py.iter(py.or2(routes, () => ([]))).map((r: any) => (py.contains(r, " ") ? py.at(py.split(r), 0) : r))));
  var queues: any = py.sorted(py.iter(py.or2(dependencies, () => ([]))).filter((d: any) => py.contains(new Set(["celery", "rq", "kafka", "rabbitmq"]), String(d).toLowerCase())).map((d: any) => d));
  var gateways: any = py.sorted(py.iter(py.or2(imports, () => ([]))).filter((imp: any) => py.truthy(py.endswith(String(imp).toLowerCase(), ["gateway", "client"]))).map((imp: any) => imp));
  var databases: any = py.sorted(py.iter(py.or2(dependencies, () => ([]))).filter((d: any) => py.contains(new Set(["sqlalchemy", "psycopg2", "mongoose", "typeorm"]), String(d).toLowerCase())).map((d: any) => d));
  return {"services": services, "apis": apis, "workers": py.sorted(py.iter(services).filter((s: any) => py.truthy(py.endswith(String(s).toLowerCase(), ["worker", "job"]))).map((s: any) => s)), "schedulers": py.sorted(py.iter(services).filter((s: any) => py.truthy(py.endswith(String(s).toLowerCase(), ["scheduler", "cron"]))).map((s: any) => s)), "queues": queues, "gateways": gateways, "databases": databases};
}
