/**
 * Converted from Python: core/evidence/semantic_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function semanticLimits(evidence_count: any, noninferable_regions: any, self_limitation: any): any {
  return {"max_confidence_without_evidence": py.F(0.45), "min_evidence_for_inference": 2, "noninferable_count": py.len(noninferable_regions), "expansion_allowed": py.get(self_limitation, "expansion_allowed", false), "reconciliation_allowed": py.get(self_limitation, "reconciliation_allowed", false)};
}
