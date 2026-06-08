/**
 * Converted from Python: core/evidence/unsupported_confidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function blockUnsupportedConfidenceEscalation(score: any, evidence_count: any, min_evidence: any = 2, max_without_evidence: any = py.F(0.45)): any {
  if (py.ge(evidence_count, min_evidence)) {
    return {"escalation_blocked": false, "capped_score": score, "reason": null};
  }
  var capped: any = py.min([score, max_without_evidence]);
  return {"escalation_blocked": py.gt(score, capped), "capped_score": py.round(capped, 3), "reason": "unsupported_confidence_escalation", "evidence_count": evidence_count};
}
