/**
 * Converted from Python: core/execution_physics/runtime_resonance_physics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_RESONANCE: any = 100000;
export function computeResonancePhysics(runtime_ir: any): any {
  var momentum: any = py.toInt((((py.get(runtime_ir, "semantic_momentum") !== null && typeof py.get(runtime_ir, "semantic_momentum") === "object" && !Array.isArray(py.get(runtime_ir, "semantic_momentum")) && !(py.get(runtime_ir, "semantic_momentum") instanceof Set) && !(py.get(runtime_ir, "semantic_momentum") instanceof Map))) ? py.get(py.get(runtime_ir, "semantic_momentum", {}), "runtime_momentum", 0) : 0));
  var entropy: any = py.toInt((((py.get(runtime_ir, "runtime_entropy") !== null && typeof py.get(runtime_ir, "runtime_entropy") === "object" && !Array.isArray(py.get(runtime_ir, "runtime_entropy")) && !(py.get(runtime_ir, "runtime_entropy") instanceof Set) && !(py.get(runtime_ir, "runtime_entropy") instanceof Map))) ? py.get(py.get(runtime_ir, "runtime_entropy", {}), "entropy_score", 0) : 0));
  var resonance: any = py.min([py.add(momentum, entropy), MAX_RESONANCE]);
  return {"resonance_amplitude": resonance, "amplified": (resonance > 500)};
}
