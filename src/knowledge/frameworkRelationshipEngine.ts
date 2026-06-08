/**
 * Converted from Python: core/knowledge/framework_relationship_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildFrameworkRelationships(frameworks: any, services: any): any {
  var fw: any = py.sorted(py.toSet(py.or2(frameworks, () => ([]))));
  var svc: any = py.sorted(py.toSet(py.or2(services, () => ([]))));
  var edges: any[] = [];
  var s: any;
  for (s of py.iter(svc)) {
    var f: any;
    for (f of py.iter(py.slice(fw, null, 3))) {
      py.listAppend(edges, {"from": s, "to": f});
    }
  }
  return {"nodes": py.sorted(py.toSet(py.add(fw, svc))), "edges": py.sorted(edges, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any})};
}
