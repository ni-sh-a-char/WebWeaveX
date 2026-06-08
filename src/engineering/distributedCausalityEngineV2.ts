/**
 * Converted from Python: core/engineering/distributed_causality_engine_v2.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CAUSALITY: any = 10000;
export function reconstructDistributedCausality(events: any): any {
  var ordered: any = py.sorted(events, {key: ((x: any) => [py.get(x, "timestamp", 0), py.toStr(py.get(x, "id"))]) as (item: any) => any});
  var edges: any[] = [];
  var idx: any;
  for (idx = 0; idx < py.sub(py.len(ordered), 1); idx++) {
    py.listAppend(edges, {"from": py.get(py.at(ordered, idx), "id"), "to": py.get(py.at(ordered, py.add(idx, 1)), "id"), "relation": "event_precedes"});
  }
  return {"causality_edges": py.slice(edges, null, MAX_CAUSALITY), "bounded": true};
}
