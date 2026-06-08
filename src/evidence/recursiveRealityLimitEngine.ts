/**
 * Converted from Python: core/evidence/recursive_reality_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recursiveRealityLimits(depth: any, entropy: any): any {
  return {"max_depth_without_evidence": 2, "closure_allowed": false, "stabilization_allowed": !py.truthy(py.get(entropy, "suppress_recursive_stabilization", false)), "current_depth": depth};
}
