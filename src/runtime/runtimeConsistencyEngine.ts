/**
 * Converted from Python: core/runtime/runtime_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";
import { proveRuntimeConsistency } from "./runtimeProofEngine.js";
import { reconcileRuntimeStates } from "./runtimeReconciliationEngine.js";

export function checkRuntimeConsistency(runtime_a: any, runtime_b: any, transitions: any = null, evidence: any = null): any {
  var recon: any = reconcileRuntimeStates(runtime_a, runtime_b);
  var proof: any = proveRuntimeConsistency(py.or2(transitions, () => ([])), py.or2(evidence, () => ([])));
  return {"reconciliation": recon, "proof": proof, "consistent": py.and2(py.eq(py.len(py.get(recon, "conflicts", [])), 0), () => (py.get(proof, "valid", false))), "deterministic": true};
}
export { proveRuntimeConsistency, reconcileRuntimeStates };
