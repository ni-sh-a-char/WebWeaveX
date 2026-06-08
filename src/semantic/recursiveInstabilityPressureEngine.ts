/**
 * Converted from Python: core/semantic/recursive_instability_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeRecursiveInstabilityPressure(instability_regions: any, depth: any): any {
  return {"pressure": py.round(py.min([py.F(1.0), py.add(py.mul(instability_regions, py.F(0.2)), py.mul(depth, py.F(0.05)))]), 3)};
}
