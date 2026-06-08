/**
 * Converted from Python: core/knowledge/ontology_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function checkOntologyConsistency(edges: any): any {
  var violations: any[] = [];
  var e: any;
  for (e of py.iter(py.or2(edges, () => ([])))) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    var ev: any = py.or2(py.get(e, "evidence", []), () => ([]));
    if (!py.truthy(ev)) {
      py.listAppend(violations, {"from": py.get(e, "from"), "to": py.get(e, "to"), "reason": "missing_evidence"});
    }
    if (py.contains(e, "type")) {
      py.listAppend(violations, {"from": py.get(e, "from"), "to": py.get(e, "to"), "reason": "forbidden_type_field"});
    }
  }
  return {"consistent": py.eq(py.len(violations), 0), "violations": violations, "edge_count": py.len(py.or2(edges, () => ([]))), "deterministic_inputs": [`violations=${py.toStr(py.len(violations))}`, `edges=${py.toStr(py.len(py.or2(edges, () => ([]))))}`]};
}
