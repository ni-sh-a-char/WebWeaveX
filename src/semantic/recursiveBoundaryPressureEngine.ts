/**
 * Converted from Python: core/semantic/recursive_boundary_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeRecursiveBoundaryPressure(boundary_erosion: any, depth: any): any {
  return {"pressure": py.round(py.min([py.F(1.0), py.add(boundary_erosion, py.mul(depth, py.F(0.06)))]), 3), "violation": (boundary_erosion >= py.F(0.3))};
}
