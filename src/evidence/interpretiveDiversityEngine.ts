/**
 * Converted from Python: core/evidence/interpretive_diversity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelInterpretiveDiversity(evidence: any, inferred: any): any {
  var interpretations: any[] = [];
  if (py.truthy(evidence)) {
    py.listAppend(interpretations, {"id": "evidence_backed", "evidence": [...py.iter(evidence)], "limitations": []});
  }
  var k: any;
  for (k of py.iter(inferred)) {
    py.listAppend(interpretations, {"id": `infer:${py.toStr(k)}`, "interpretation": {[py.toStr(k)]: py.at(inferred, k)}, "evidence": [...py.iter(evidence)], "limitations": (!py.contains(evidence, k) ? ["inferred"] : []), "contradictions": [], "ambiguities": [], "plurality": {"rank": ((py.len(evidence) < 2) ? "secondary" : "primary")}, "confidence": {"capped": (py.len(evidence) < 2)}});
  }
  return {"preserved": true, "count": py.len(interpretations), "interpretations": py.slice(interpretations, null, 10)};
}
