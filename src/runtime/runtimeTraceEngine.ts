/**
 * Converted from Python: core/runtime/runtime_trace_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_TRACE_ENTRIES: any = 1000;
export function buildRuntimeTrace(steps: any, parser_evidence: any): any {
  var bounded: any = py.slice(py.sorted(steps, {key: ((s: any) => py.toInt(py.get(s, "order", 0))) as (item: any) => any}), null, MAX_TRACE_ENTRIES);
  return {"trace": py.iter(bounded).map((s: any) => ({"id": py.get(s, "id"), "label": py.get(s, "label"), "order": py.get(s, "order")})), "count": py.len(bounded), "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true, "bounded": (py.len(bounded) <= MAX_TRACE_ENTRIES)};
}
