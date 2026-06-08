/**
 * Converted from Python: core/evidence/semantic_dependency_calculus.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function deriveDependency(from_keys: any, to_keys: any, evidence: any): any {
  var ev: any = py.sorted(py.toSet(py.iter(evidence).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var derivable: any = py.and2(py.truthy(from_keys), () => (py.and2(py.truthy(to_keys), () => ((py.len(ev) >= 1)))));
  return {"derivable": derivable, "from": [...py.iter(from_keys)], "to": [...py.iter(to_keys)], "evidence": ev, "rule": "dependency_requires_evidence", "deterministic_inputs": [`evidence=${py.toStr(py.len(ev))}`]};
}
