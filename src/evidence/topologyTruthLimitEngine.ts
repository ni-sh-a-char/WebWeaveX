/**
 * Converted from Python: core/evidence/topology_truth_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function topologyTruthLimits(boundaries: any): any {
  return {"self_confirmation_allowed": false, "propagation": py.get(boundaries, "propagation_allowed", false)};
}
