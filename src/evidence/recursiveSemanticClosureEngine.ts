/**
 * Converted from Python: core/evidence/recursive_semantic_closure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _closureRecord(reason: any, depth: any): any {
  return {"reason": reason, "recursive_pressure": {"depth": depth, "level": py.min([py.F(1.0), py.mul(depth, py.F(0.12))])}, "closure_pressure": {"level": py.F(0.8)}, "confidence_decay": {"required": true}, "entropy_pressure": {"preserve": true}, "truth_boundary_violation": {"type": "recursive_semantic_closure"}, "recursive_instability": {"preserved": true}};
}
export function detectRecursiveSemanticClosure(depth: any, inferred: any, reconciled: any, evidence: any): any {
  var suppressed: any[] = [];
  if (((depth >= 2) && py.eq(reconciled, inferred) && (py.len(evidence) < 2))) {
    py.listAppend(suppressed, _closureRecord("recursive_coherence_closure", depth));
  }
  if (((depth >= 3) && (py.len(inferred) > py.add(py.len(evidence), depth)))) {
    py.listAppend(suppressed, _closureRecord("recursive_inference_amplification", depth));
  }
  return {"closure_detected": py.truthy(suppressed), "suppressed_closures": suppressed, "closure_pressure": py.round(py.min([py.F(1.0), py.mul(depth, py.F(0.15))]), 3)};
}
