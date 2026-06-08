/**
 * Converted from Python: core/evidence/semantic_monoculture_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _suppressionRecord(reason: any): any {
  return {"reason": reason, "plurality_pressure": {"preserve": true}, "monoculture_pressure": {"level": py.F(0.9)}, "orthodoxy_pressure": {"level": py.F(0.8)}, "closure_pressure": {"level": py.F(0.7)}, "interpretive_diversity": {"required": true}, "explanatory_diversity": {"required": true}};
}
export function detectSemanticMonoculture(interpretations: any, evidence: any, depth: any): any {
  var suppressed: any[] = [];
  if (((py.len(interpretations) <= 1) && (depth >= 2) && (py.len(evidence) < 2))) {
    py.listAppend(suppressed, _suppressionRecord("semantic_monoculture"));
  }
  return {"detected": py.truthy(suppressed), "suppressed": suppressed};
}
