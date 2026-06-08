/**
 * Converted from Python: core/knowledge/semantic_merge_rigor_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function mergeWithEvidence(sources: any): any {
  var merged_evidence: any[] = [];
  var s: any;
  for (s of py.iter(py.or2(sources, () => ([])))) {
    var ev: any = py.or2(py.get(s, "evidence", []), () => ([]));
    if ((typeof ev === "string")) {
      ev = [ev];
    }
    if (!py.truthy(ev)) {
      return {"merged": false, "reason": "silent_merge_forbidden", "sources": py.len(py.or2(sources, () => ([])))};
    }
    py.extend(merged_evidence, py.iter(ev).map((e: any) => py.toStr(e)));
  }
  return {"merged": true, "evidence": py.sorted(py.toSet(merged_evidence)), "source_count": py.len(py.or2(sources, () => ([]))), "deterministic_inputs": [`sources=${py.toStr(py.len(py.or2(sources, () => ([]))))}`]};
}
