/**
 * Converted from Python: core/evidence/epistemic_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveEpistemicBoundaries(evidence: any, noninferable_regions: any, unstable_regions: any): any {
  return {"visible": true, "where_inference_stops": noninferable_regions, "where_cognition_stops": unstable_regions, "where_reconstruction_stops": unstable_regions, "suppress_stabilization": py.truthy(unstable_regions), "suppress_coherence": (py.len(evidence) < 2)};
}
