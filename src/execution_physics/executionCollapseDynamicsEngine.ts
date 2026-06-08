/**
 * Converted from Python: core/execution_physics/execution_collapse_dynamics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let COLLAPSE_THRESHOLD: any = 10000;
export function analyzeCollapseDynamics(runtime_ir: any): any {
  var pressure: any = py.toInt((((py.get(runtime_ir, "execution_physics") !== null && typeof py.get(runtime_ir, "execution_physics") === "object" && !Array.isArray(py.get(runtime_ir, "execution_physics")) && !(py.get(runtime_ir, "execution_physics") instanceof Set) && !(py.get(runtime_ir, "execution_physics") instanceof Map))) ? py.get(py.get(runtime_ir, "execution_physics", {}), "execution_pressure", 0) : 0));
  var collapse_risk: any = (py.gt(pressure, COLLAPSE_THRESHOLD) ? "imminent" : "contained");
  return {"collapse_risk": collapse_risk, "pressure": pressure};
}
