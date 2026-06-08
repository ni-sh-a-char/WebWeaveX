/**
 * Converted from Python: core/causality/runtime_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeCausality(events: any, origins: any): any {
  var ordered: any = py.sorted(events, {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any});
  var causal_edges: any[] = [];
  var index: any;
  for (index = 1; index < py.len(ordered); index++) {
    var prev_id: any = py.toStr(py.get(py.at(ordered, py.sub(index, 1)), "id", `evt:${py.toStr(py.sub(index, 1))}`));
    var curr_id: any = py.toStr(py.get(py.at(ordered, index), "id", `evt:${py.toStr(index)}`));
    py.listAppend(causal_edges, {"from": prev_id, "to": curr_id, "relation": "propagates"});
  }
  var propagation_order: any = py.iter(ordered).map((event: any) => py.toStr(py.get(event, "id", "")));
  return {"events": ordered, "causal_edges": causal_edges, "runtime_origins": py.pyDict(origins), "propagation_order": propagation_order, "bounded": true};
}
