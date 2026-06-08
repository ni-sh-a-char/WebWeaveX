/**
 * Converted from Python: core/evidence/semantic_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticBoundaries(inferred: any, allowed: any): any {
  return {"inference_allowed": allowed, "bounded_inferences": (py.truthy(allowed) ? py.sorted(py.keys(inferred)) : []), "blocked_inferences": (!py.truthy(allowed) ? py.sorted(py.keys(inferred)) : []), "where_inference_stops": (py.truthy(allowed) ? [] : py.sorted(py.keys(inferred))), "reality_bounded": allowed};
}
