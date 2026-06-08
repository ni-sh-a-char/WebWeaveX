/**
 * Converted from Python: core/semantic/recursive_convergence_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeRecursiveConvergencePressure(depth: any, diversity_score: any): any {
  var pressure: any = py.round(py.min([py.F(1.0), py.add(py.mul(depth, py.F(0.08)), py.max([0, py.sub(py.F(0.5), diversity_score)]))]), 3);
  return {"pressure": pressure, "suppress": (pressure >= py.F(0.3))};
}
