/**
 * Converted from Python: core/repository/orchestration_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reasonOrchestration(services: any, dependencies: any): any {
  var svc: any = py.sorted(py.toSet(py.iter(py.or2(services, () => ([]))).filter((s: any) => py.truthy(s)).map((s: any) => py.toStr(s))));
  var deps: any = py.sorted(py.toSet(py.iter(py.or2(dependencies, () => ([]))).filter((d: any) => py.truthy(d)).map((d: any) => py.toStr(d))));
  var edges: any = py.range(py.sub(py.len(svc), 1)).map((i: any) => ({"from": py.at(svc, i), "to": py.at(svc, py.add(i, 1))}));
  return {"services": svc, "dependencies": deps, "flow_edges": edges};
}
