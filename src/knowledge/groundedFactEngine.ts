/**
 * Converted from Python: core/knowledge/grounded_fact_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildGroundedFacts(edges: any, evidence_key: any = "evidence"): any {
  var facts: any[] = [];
  var edge: any;
  for (edge of py.iter(py.or2(edges, () => ([])))) {
    if (!((edge !== null && typeof edge === "object" && !Array.isArray(edge) && !(edge instanceof Set) && !(edge instanceof Map)))) {
      continue;
    }
    const _d1 = py.iter([py.get(edge, "from"), py.get(edge, "to")]) as any[];
    var f: any = _d1[0];
    var t: any = _d1[1];
    if ((!py.truthy(f) || !py.truthy(t))) {
      continue;
    }
    py.listAppend(facts, {"subject": py.toStr(f), "object": py.toStr(t), "relation": "related_to", [py.toStr(evidence_key)]: py.get(edge, evidence_key, "graph_edge")});
  }
  return py.sorted(facts, {key: ((x: any) => [py.at(x, "subject"), py.at(x, "object")]) as (item: any) => any});
}
