/**
 * Converted from Python: core/evidence/semantic_truth_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function semanticTruthLimits(entropy: any, instability: any): any {
  return {"stabilization_allowed": !py.truthy(py.get(entropy, "suppress_stabilization", false)), "coherence_allowed": !py.truthy(py.get(entropy, "suppress_coherence", false)), "instability_preserved": py.get(instability, "preserved", true)};
}
