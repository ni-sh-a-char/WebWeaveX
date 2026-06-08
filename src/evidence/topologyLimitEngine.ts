/**
 * Converted from Python: core/evidence/topology_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function topologyLimits(boundaries: any): any {
  return {"propagation": py.get(boundaries, "propagation_allowed", false), "deployment": py.get(boundaries, "deployment_inference_allowed", false)};
}
