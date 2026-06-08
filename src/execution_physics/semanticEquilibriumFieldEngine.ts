/**
 * Converted from Python: core/execution_physics/semantic_equilibrium_field_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildEquilibriumField(runtime_ir: any): any {
  var physics: any = py.get(runtime_ir, "execution_physics", {});
  var pressure: any = py.toInt((((physics !== null && typeof physics === "object" && !Array.isArray(physics) && !(physics instanceof Set) && !(physics instanceof Map))) ? py.get(physics, "execution_pressure", 0) : 0));
  var field_state: any = ((pressure < 1000) ? "equilibrium" : "disequilibrium");
  return {"field_state": field_state, "field_pressure": pressure};
}
