/**
 * Converted from Python: core/evidence/contradiction_evidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectContradictionEvidence(snippets: any): any {
  var normalized: Record<string, any> = {};
  var idx: any;
  var text: any;
  for ([idx, text] of py.enumerate(py.or2(snippets, () => ([])))) {
    var lower: any = String(py.or2(text, () => (""))).toLowerCase();
    var token: any;
    for (token of py.iter(["true", "false", "enabled", "disabled", "deprecated", "stable"])) {
      if (py.contains(lower, token)) {
        py.setAdd(py.setdefault(normalized, token, new Set()), idx);
      }
    }
  }
  var pairs: any[] = [];
  var conflicts: any[] = [];
  var opposites: any = [["true", "false"], ["enabled", "disabled"], ["deprecated", "stable"]];
  var a: any;
  var b: any;
  for ([a, b] of py.iter(opposites)) {
    if ((py.contains(normalized, a) && py.contains(normalized, b))) {
      py.listAppend(pairs, [a, b]);
      py.listAppend(conflicts, {"polarity_a": a, "polarity_b": b, "snippet_indices_a": py.sorted(py.at(normalized, a)), "snippet_indices_b": py.sorted(py.at(normalized, b)), "evidence": "polarity_conflict"});
    }
  }
  return {"contradiction_pairs": pairs, "conflicts": conflicts, "evidence": ["deterministic_polarity_scan"], "sources": py.iter(py.sorted(py.toSet(py.values(normalized).flatMap((s: any) => py.iter(s).map((i: any) => i))))).map((i: any) => `snippet:${py.toStr(i)}`), "grounding": {"method": "polarity_token_scan"}, "lineage": {"stage": "contradiction_evidence"}, "confidence_basis": {"conflict_count": py.len(conflicts)}};
}
