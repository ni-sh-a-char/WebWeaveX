/**
 * Converted from Python: core/evidence/insufficiency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function markInsufficiency(bundle: any, min_evidence: any = 2): any {
  var evidence: any = py.or2(py.get(bundle, "evidence", []), () => ([]));
  var insufficient: any = (py.len(evidence) < min_evidence);
  var flags: any[] = [];
  if (py.truthy(insufficient)) {
    py.listAppend(flags, "insufficient_evidence");
  }
  if (py.truthy(py.get(bundle, "ambiguities"))) {
    py.listAppend(flags, "ambiguous_claim");
  }
  return {"insufficient": insufficient, "flags": py.sorted(py.toSet(flags)), "evidence_count": py.len(evidence), "required": min_evidence, "message": (py.truthy(insufficient) ? "insufficient evidence" : "evidence_ok")};
}
