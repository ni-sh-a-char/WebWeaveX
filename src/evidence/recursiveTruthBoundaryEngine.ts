/**
 * Converted from Python: core/evidence/recursive_truth_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelRecursiveTruthBoundaries(depth: any, evidence_count: any, min_evidence: any = 2): any {
  var erosion: any = py.round(py.min([py.F(1.0), py.mul(depth, py.F(0.08))]), 3);
  var bounded: any = py.and2(py.ge(evidence_count, min_evidence), () => ((erosion < py.F(0.5))));
  return {"bounded": bounded, "depth": depth, "erosion": erosion, "closure_allowed": false, "recursive_lock_in_allowed": false};
}
