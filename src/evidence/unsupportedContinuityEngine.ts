/**
 * Converted from Python: core/evidence/unsupported_continuity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _continuationRecord(reason: any, evidence_gap: any): any {
  return {"reason": reason, "boundary_violation": {"type": "unsupported_continuity"}, "evidence_gap": evidence_gap, "semantic_instability": {"unstable": true}, "fragility": {"level": py.F(0.7)}, "confidence_caps": {"max": py.F(0.4)}};
}
export function suppressUnsupportedContinuity(label: any, evidence: any, min_evidence: any = 2): any {
  var gap: any = {"required": min_evidence, "actual": py.len(evidence)};
  if ((py.len(evidence) < min_evidence)) {
    return {"suppressed": true, "record": _continuationRecord(`continuity:${py.toStr(label)}`, gap)};
  }
  return {"suppressed": false, "record": null};
}
export function collectUnsupportedContinuity(evidence: any, inferred: any, reconciled: any): any {
  var out: any[] = [];
  var k: any;
  for (k of py.iter(inferred)) {
    var r: any = suppressUnsupportedContinuity(`infer:${py.toStr(k)}`, evidence);
    if ((py.truthy(py.at(r, "suppressed")) && py.truthy(py.at(r, "record")))) {
      py.listAppend(out, py.at(r, "record"));
    }
  }
  if ((py.truthy(reconciled) && (py.len(evidence) < 2))) {
    r = suppressUnsupportedContinuity("reconcile", evidence);
    if ((py.truthy(py.at(r, "suppressed")) && py.truthy(py.at(r, "record")))) {
      py.listAppend(out, py.at(r, "record"));
    }
  }
  return out;
}
