/**
 * Converted from Python: core/evidence/uncertainty_visibility_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function exposeUncertaintyVisibility(uncertainties: any, ambiguities: any, confidence_score: any): any {
  var pressure: any = py.round(py.min([py.F(1.0), py.add(py.mul(py.len(uncertainties), py.F(0.15)), py.mul(py.len(ambiguities), py.F(0.1)))]), 3);
  return {"visible": py.truthy(py.or2(uncertainties, () => (ambiguities))), "count": py.len(uncertainties), "items": py.sorted(py.toSet(py.iter(uncertainties).map((u: any) => py.toStr(u)))), "pressure": pressure, "suppress_propagation": (pressure >= py.F(0.3)), "confidence_impact": py.round(py.min([py.F(0.35), py.mul(pressure, py.F(0.4))]), 3), "preserved": true};
}
