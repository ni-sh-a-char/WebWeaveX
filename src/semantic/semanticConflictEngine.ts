/**
 * Converted from Python: core/semantic/semantic_conflict_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectSemanticConflicts(claims: any): any {
  var keys: Record<string, any> = {};
  var claim: any;
  for (claim of py.iter(py.or2(claims, () => ([])))) {
    if (!((claim !== null && typeof claim === "object" && !Array.isArray(claim) && !(claim instanceof Set) && !(claim instanceof Map)))) {
      continue;
    }
    var k: any = py.toStr(py.get(claim, "key", ""));
    var v: any = py.toStr(py.get(claim, "value", ""));
    py.setAdd(py.setdefault(keys, k, new Set()), v);
  }
  var conflicts: any = py.iter(py.sorted(py.items(keys))).filter(([k, v]: any) => (py.len(v) > 1)).map(([k, v]: any) => ({"key": k, "values": py.sorted(v)}));
  return {"conflicts": conflicts, "evidence": ["semantic_conflict_scan"], "sources": py.sorted(py.toSet(py.iter(py.or2(claims, () => ([]))).filter((c: any) => ((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map)))).map((c: any) => py.toStr(py.get(c, "source", ""))))), "grounding": {"method": "value_multiplicity"}, "lineage": {"stage": "semantic_conflict"}};
}
