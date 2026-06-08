/**
 * Converted from Python: core/evidence/inference_refusal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function refuseInference(reasons: any, evidence_count: any): any {
  return {"refused": true, "reasons": py.sorted(py.toSet(reasons)), "evidence_count": evidence_count, "message": ((evidence_count < 2) ? "cannot_conclude" : "conclude_with_caution")};
}
