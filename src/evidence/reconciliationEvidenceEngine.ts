/**
 * Converted from Python: core/evidence/reconciliation_evidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconcileEvidence(claims: any): any {
  var by_key: Record<string, any> = {};
  var claim: any;
  for (claim of py.iter(py.or2(claims, () => ([])))) {
    if (!((claim !== null && typeof claim === "object" && !Array.isArray(claim) && !(claim instanceof Set) && !(claim instanceof Map)))) {
      continue;
    }
    var key: any = py.toStr(py.get(claim, "key", py.get(claim, "id", "")));
    py.listAppend(py.setdefault(by_key, key, []), claim);
  }
  var reconciled: any[] = [];
  var conflicts: any[] = [];
  var group: any;
  for ([key, group] of py.iter(py.sorted(py.items(by_key)))) {
    var values: any = py.sorted(py.toSet(py.iter(group).map((c: any) => py.toStr(py.get(c, "value", "")))));
    if ((py.len(values) > 1)) {
      py.listAppend(conflicts, {"key": key, "values": values, "claims": py.len(group)});
    }
    var winner: any = (py.truthy(values) ? py.at(values, 0) : "");
    py.listAppend(reconciled, {"key": key, "value": winner, "claim_count": py.len(group)});
  }
  return {"reconciled": reconciled, "conflicts": conflicts, "evidence": ["evidence_reconciliation"], "sources": py.sorted(py.toSet(py.values(by_key).flatMap((g: any) => py.iter(g).filter((c: any) => py.truthy(py.get(c, "source"))).map((c: any) => py.toStr(py.get(c, "source", "")))))), "grounding": {"method": "deterministic_lexicographic_winner"}, "lineage": {"stage": "reconciliation"}};
}
