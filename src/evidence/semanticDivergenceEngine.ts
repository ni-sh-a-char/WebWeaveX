/**
 * Converted from Python: core/evidence/semantic_divergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticDivergence(observed: any, inferred: any, ambiguities: any): any {
  var keys: any = py.bitor(py.toSet(py.keys(observed)), py.toSet(py.keys(inferred)));
  var score: any = py.round(py.min([py.F(1.0), py.add(py.mul(py.len(keys), py.F(0.15)), py.mul(py.len(ambiguities), py.F(0.1)))]), 3);
  return {"divergence_score": score, "preserved": py.or2((score > 0), () => (py.truthy(ambiguities))), "phase_space_maintained": (py.len(keys) > 1)};
}
