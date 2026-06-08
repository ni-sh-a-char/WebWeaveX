/**
 * Converted from Python: core/evidence/semantic_diversity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticDiversity(observed: any, inferred: any, ambiguities: any): any {
  var score: any = py.round(py.min([py.F(1.0), py.mul(py.add(py.add(py.len(observed), py.len(inferred)), py.len(ambiguities)), py.F(0.1))]), 3);
  return {"diversity_score": score, "preserved": py.or2((score > 0), () => (py.truthy(ambiguities)))};
}
