/**
 * Converted from Python: core/execution_physics/runtime_turbulence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let TURBULENCE_THRESHOLD: any = 1000;
export function analyzeRuntimeTurbulence(runtime_ir: any): any {
  var entropy: any = py.get(runtime_ir, "runtime_entropy", {});
  var entropy_score: any = py.toInt((((entropy !== null && typeof entropy === "object" && !Array.isArray(entropy) && !(entropy instanceof Set) && !(entropy instanceof Map))) ? py.get(entropy, "entropy_score", 0) : 0));
  var turbulence: any = (py.gt(entropy_score, TURBULENCE_THRESHOLD) ? "high" : "low");
  return {"runtime_turbulence": turbulence, "entropy_score": entropy_score};
}
