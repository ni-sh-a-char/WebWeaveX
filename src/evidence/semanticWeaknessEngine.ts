/**
 * Converted from Python: core/evidence/semantic_weakness_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWeaknesses(evidence: any, ambiguities: any, min_evidence: any = 2): any {
  var weaknesses: any[] = [];
  if ((py.len(evidence) < min_evidence)) {
    py.listAppend(weaknesses, "insufficient_evidence");
  }
  var a: any;
  for (a of py.iter(py.or2(ambiguities, () => ([])))) {
    py.listAppend(weaknesses, `ambiguity:${py.toStr(a)}`);
  }
  return {"weaknesses": py.sorted(py.toSet(weaknesses)), "weak_evidence": (py.len(evidence) < min_evidence), "weakness_count": py.len(weaknesses)};
}
