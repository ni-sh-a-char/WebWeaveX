/**
 * Converted from Python: core/semantic/recursive_dependency_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeRecursiveDependencyPressure(depth: any, interpretation_count: any): any {
  var pressure: any = py.round(py.min([py.F(1.0), py.add(py.mul(py.max([0, py.sub(depth, 1)]), py.F(0.15)), ((interpretation_count <= 1) ? py.F(0.2) : 0))]), 3);
  return {"pressure": pressure, "violation": (pressure >= py.F(0.3))};
}
