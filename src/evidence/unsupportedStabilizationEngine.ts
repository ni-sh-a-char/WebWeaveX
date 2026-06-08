/**
 * Converted from Python: core/evidence/unsupported_stabilization_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _stabilizationRecord(reason: any, evidence_gap: any): any {
  return {"reason": reason, "reinforcement_pressure": {"level": py.F(0.8)}, "evidence_gap": evidence_gap, "semantic_instability": {"preserved": true, "unstable": true}, "truth_boundary_violation": {"type": "unsupported_stabilization"}, "confidence_collapse": {"required": true}};
}
export function detectUnsupportedStabilization(evidence: any, inferred: any, reconciled: any, min_evidence: any = 2): any {
  var suppressed: any[] = [];
  var gap: any = {"required": min_evidence, "actual": py.len(evidence)};
  if ((py.eq(reconciled, inferred) && (py.len(evidence) < min_evidence) && py.truthy(inferred))) {
    py.listAppend(suppressed, _stabilizationRecord("coherence_stabilization", gap));
  }
  if ((py.len(inferred) > py.add(py.len(evidence), 1))) {
    py.listAppend(suppressed, _stabilizationRecord("inference_confirming_inference", gap));
  }
  return {"stabilization_detected": py.truthy(suppressed), "suppressed_stabilizations": suppressed, "count": py.len(suppressed)};
}
