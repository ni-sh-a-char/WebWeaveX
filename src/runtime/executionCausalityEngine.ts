/**
 * Converted from Python: core/runtime/execution_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_CAUSALITY_EDGES: any = 500;
export function reconstructExecutionCausality(events: any, parser_evidence: any): any {
  var ordered: any = py.slice(py.sorted(events, {key: ((e: any) => [py.toInt(py.get(e, "order", 0)), py.toStr(py.get(e, "id", ""))]) as (item: any) => any}), null, MAX_CAUSALITY_EDGES);
  var edges: any[] = [];
  var idx: any;
  for (idx = 1; idx < py.len(ordered); idx++) {
    const _d1 = py.iter([py.at(ordered, py.sub(idx, 1)), py.at(ordered, idx)]) as any[];
    var prev_e: any = _d1[0];
    var cur_e: any = _d1[1];
    py.listAppend(edges, {"from": py.get(prev_e, "id"), "to": py.get(cur_e, "id"), "metadata": {"kind": "execution_cause", "basis": "event_order"}});
  }
  return {"edges": edges, "count": py.len(edges), "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true, "bounded": (py.len(edges) <= MAX_CAUSALITY_EDGES)};
}
