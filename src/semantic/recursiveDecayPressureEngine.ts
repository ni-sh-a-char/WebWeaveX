/**
 * Converted from Python: core/semantic/recursive_decay_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeRecursiveDecayPressure(depth: any): any {
  return {"pressure": py.round(py.min([py.F(1.0), py.mul(depth, py.F(0.1))]), 3), "depth": depth};
}
