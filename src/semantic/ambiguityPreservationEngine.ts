/**
 * Converted from Python: core/semantic/ambiguity_preservation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveAmbiguities(candidates: any, evidence: any): any {
  var unique: any = py.sorted(py.toSet(py.iter(py.or2(candidates, () => ([]))).filter((c: any) => py.truthy(c)).map((c: any) => py.toStr(c))));
  var unresolved: any = ((py.len(unique) > 1) ? unique : []);
  return {"ambiguities": unresolved, "preserved": py.truthy(unresolved), "evidence": py.sorted(py.toSet(py.or2(evidence, () => ([])))), "lineage": {"stage": "ambiguity_preservation", "count": py.len(unresolved)}};
}
