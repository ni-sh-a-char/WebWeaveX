/**
 * Converted from Python: core/execution_physics/semantic_runtime_thermodynamics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function analyzeRuntimeThermodynamics(runtime_ir: any): any {
  var pressure: any = py.toInt((((py.get(runtime_ir, "execution_physics") !== null && typeof py.get(runtime_ir, "execution_physics") === "object" && !Array.isArray(py.get(runtime_ir, "execution_physics")) && !(py.get(runtime_ir, "execution_physics") instanceof Set) && !(py.get(runtime_ir, "execution_physics") instanceof Map))) ? py.get(py.get(runtime_ir, "execution_physics", {}), "execution_pressure", 0) : 0));
  var entropy: any = py.toInt((((py.get(runtime_ir, "runtime_entropy") !== null && typeof py.get(runtime_ir, "runtime_entropy") === "object" && !Array.isArray(py.get(runtime_ir, "runtime_entropy")) && !(py.get(runtime_ir, "runtime_entropy") instanceof Set) && !(py.get(runtime_ir, "runtime_entropy") instanceof Map))) ? py.get(py.get(runtime_ir, "runtime_entropy", {}), "entropy_score", 0) : 0));
  var temperature: any = py.min([py.add(pressure, entropy), 100000]);
  return {"temperature": temperature, "thermodynamic_state": ((temperature > 1000) ? "hot" : "cool")};
}
