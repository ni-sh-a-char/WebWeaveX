/**
 * Converted from Python: core/evidence/semantic_plurality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticPlurality(observed: any, inferred: any, ambiguities: any, contradicted: any): any {
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var alt_count: any = py.add(py.add(py.len(py.bitor(py.toSet(py.keys(observed)), py.toSet(py.keys(inferred)))), py.len(ambiguities)), py.len(pairs));
  return {"preserved": true, "alternative_count": alt_count, "unresolved": py.truthy(py.or2(ambiguities, () => (pairs))), "monoculture_risk": py.and2((alt_count < 2), () => (!py.truthy(pairs)))};
}
