/**
 * Converted from Python: core/semantic/uncertainty_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeUncertaintyPressure(uncertainties: any, ambiguities: any): any {
  var count: any = py.add(py.len(uncertainties), py.len(ambiguities));
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(count, py.F(0.1))]), 3);
  return {"pressure": pressure, "suppress_propagation": (pressure >= py.F(0.25)), "confidence_reduction": py.round(py.min([py.F(0.3), py.mul(pressure, py.F(0.35))]), 3), "preserved": true};
}
