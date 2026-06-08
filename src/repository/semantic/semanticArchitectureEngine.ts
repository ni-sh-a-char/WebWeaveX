/**
 * Converted from Python: core/repository/semantic/semantic_architecture_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function reconstructSemanticArchitecture(services: any, dependencies: any, imports: any, routes: any): any {
  var deps: any = py.toSet(py.iter(py.or2(dependencies, () => ([]))).map((d: any) => String(d).toLowerCase()));
  var svc_count: any = py.len(py.get(py.or2(services, () => ({})), "services", []));
  var route_count: any = py.len(py.or2(routes, () => ([])));
  var styles: any = ["monolith"];
  if ((svc_count >= 5)) {
    py.listAppend(styles, "microservices");
  }
  if (py.truthy(py.bitand(new Set(["kafka", "rabbitmq", "celery", "rq"]), deps))) {
    py.listAppend(styles, "event-driven");
  }
  if (((route_count > 0) && (svc_count > 0))) {
    py.listAppend(styles, "layered");
  }
  if (py.any(py.iter(py.or2(imports, () => ([]))).map((i: any) => py.or2(py.contains(String(i).toLowerCase(), "command"), () => (py.contains(String(i).toLowerCase(), "query")))))) {
    py.listAppend(styles, "cqrs");
  }
  if (py.truthy(py.bitand(new Set(["aws-lambda", "serverless"]), deps))) {
    py.listAppend(styles, "serverless");
  }
  var relationships: any[] = [];
  var api: any;
  for (api of py.iter(py.get(py.or2(services, () => ({})), "apis", []))) {
    py.listAppend(relationships, {"from": "api", "to": api});
  }
  var db: any;
  for (db of py.iter(py.get(py.or2(services, () => ({})), "databases", []))) {
    py.listAppend(relationships, {"from": "service", "to": db});
  }
  return {"styles": py.sorted(py.toSet(styles)), "relationships": py.sorted(relationships, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any})};
}
