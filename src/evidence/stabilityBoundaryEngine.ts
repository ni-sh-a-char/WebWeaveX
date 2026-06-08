/**
 * Converted from Python: core/evidence/stability_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelStabilityBoundary(unstable_regions: any): any {
  return {"broken": py.truthy(unstable_regions), "regions": unstable_regions, "suppress_stabilization": py.truthy(unstable_regions)};
}
