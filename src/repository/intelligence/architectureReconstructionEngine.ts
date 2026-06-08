/**
 * Converted from Python: core/repository/intelligence/architecture_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function reconstructArchitecture(topology: any, imports: any, routes: any, dependencies: any): any {
  var services: any = py.sorted(py.toSet(py.get(topology, "services", [])));
  var db: any = py.sorted(py.toSet(py.iter(py.or2(dependencies, () => ([]))).filter((d: any) => py.any(py.iter(["postgres", "mysql", "sqlite", "mongo"]).map((k: any) => py.contains(String(d).toLowerCase(), k)))).map((d: any) => d)));
  var frontend: any = py.any(py.iter(py.or2(dependencies, () => ([]))).map((d: any) => py.any(py.iter(["react", "vue", "angular", "next"]).map((k: any) => py.contains(String(d).toLowerCase(), k)))));
  var backend: any = py.any(py.iter(py.or2(dependencies, () => ([]))).map((d: any) => py.any(py.iter(["flask", "django", "fastapi", "express", "spring"]).map((k: any) => py.contains(String(d).toLowerCase(), k)))));
  return {"services": services, "apis": py.sorted(py.toSet(py.or2(routes, () => ([])))), "workers": [], "schedulers": [], "queues": [], "gateways": [], "databases": db, "frontend_backend_split": {"frontend": frontend, "backend": backend}, "relationships": py.range(py.max([0, py.sub(py.len(services), 1)])).map((i: any) => ({"from": py.at(services, i), "to": py.at(services, py.add(i, 1))}))};
}
