/**
 * Converted from Python: core/evidence/ambiguity_visibility_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function exposeAmbiguityVisibility(ambiguities: any, confidence_score: any): any {
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(py.len(ambiguities), py.F(0.12))]), 3);
  return {"visible": py.truthy(ambiguities), "count": py.len(ambiguities), "items": py.sorted(py.toSet(py.iter(ambiguities).map((a: any) => py.toStr(a)))), "pressure": pressure, "suppress_expansion": (pressure >= py.F(0.25)), "confidence_impact": py.round(py.min([py.F(0.3), py.mul(pressure, py.F(0.35))]), 3), "preserved": true};
}
