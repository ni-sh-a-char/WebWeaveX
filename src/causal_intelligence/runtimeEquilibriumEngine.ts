/**
 * Converted from Python: core/causal_intelligence/runtime_equilibrium_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let EQUILIBRIUM_ENTROPY_THRESHOLD: any = 100;
export function computeRuntimeEquilibrium(runtime_ir: any): any {
  var entropy: any = py.get(runtime_ir, "runtime_entropy", {});
  var entropy_score: any = py.toInt(py.get(entropy, "entropy_score", 0));
  var equilibrium: any = (py.lt(entropy_score, EQUILIBRIUM_ENTROPY_THRESHOLD) ? "stable" : "unstable");
  return {"equilibrium": equilibrium, "entropy_score": entropy_score};
}
