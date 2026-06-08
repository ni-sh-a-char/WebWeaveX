/**
 * Converted from Python: core/semantic/ambiguity_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeAmbiguityPressure(ambiguities: any): any {
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(py.len(ambiguities), py.F(0.12))]), 3);
  return {"pressure": pressure, "suppress_expansion": (pressure >= py.F(0.2)), "confidence_reduction": py.round(py.min([py.F(0.25), py.mul(pressure, py.F(0.3))]), 3), "preserved": true};
}
