/**
 * Converted from Python: core/evidence/semantic_proof_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function proveSemanticClaim(claim: any, evidence: any, min_evidence: any = 1): any {
  var ev: any = py.sorted(py.toSet(py.iter(evidence).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var proved: any = (py.len(ev) >= min_evidence);
  return {"claim": claim, "proved": proved, "evidence": ev, "steps": [{"rule": "evidence_threshold", "met": proved}], "deterministic_inputs": [`evidence=${py.toStr(py.len(ev))}`, `min=${py.toStr(min_evidence)}`]};
}
