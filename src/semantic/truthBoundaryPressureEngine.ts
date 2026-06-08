/**
 * Converted from Python: core/semantic/truth_boundary_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeTruthBoundaryPressure(truth_bounded: any, entropy: any): any {
  var pressure: any = py.round(py.add((py.truthy(truth_bounded) ? py.F(0.0) : py.F(0.5)), py.mul(entropy, py.F(0.3))), 3);
  return {"pressure": py.min([py.F(1.0), pressure]), "violation": !py.truthy(truth_bounded)};
}
