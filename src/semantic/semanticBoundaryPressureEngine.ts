/**
 * Converted from Python: core/semantic/semantic_boundary_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeSemanticBoundaryPressure(boundary_pressure: any, drift_pressure: any): any {
  var pressure: any = py.round(py.min([py.F(1.0), py.add(boundary_pressure, py.mul(drift_pressure, py.F(0.5)))]), 3);
  return {"pressure": pressure, "suppress_continuation": (pressure >= py.F(0.25))};
}
