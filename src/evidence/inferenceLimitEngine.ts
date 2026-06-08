/**
 * Converted from Python: core/evidence/inference_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelSemanticBoundaries } from "./semanticBoundaryEngine.js";

export function modelInferenceLimits(inferred: any, evidence_count: any): any {
  var allowed: any = (evidence_count >= 2);
  var boundaries: any = modelSemanticBoundaries(inferred, allowed);
  return {...(boundaries), "max_inferred_keys": (py.truthy(allowed) ? py.len(inferred) : 0), "evidence_required": 2};
}
export { modelSemanticBoundaries };
