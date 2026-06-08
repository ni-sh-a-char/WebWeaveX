/**
 * Converted from Python: core/causality/causal_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recoverCausalRuntime(causality: any, events: any): any {
  var propagation_order: any = [...py.iter(py.get(causality, "propagation_order", []))];
  var recovered_events: any = [...py.iter(events)];
  if ((!py.truthy(propagation_order) && py.truthy(events))) {
    propagation_order = py.iter(events).map((event: any) => py.toStr(py.get(event, "id", "")));
  }
  var gaps: any[] = [];
  var index: any;
  for (index = 1; index < py.len(propagation_order); index++) {
    if (!py.truthy(py.at(propagation_order, index))) {
      py.listAppend(gaps, index);
    }
  }
  var gap_index: any;
  for (gap_index of py.iter(gaps)) {
    py.listAppend(recovered_events, {"id": `recovered:evt:${py.toStr(gap_index)}`, "runtime": "recovery", "type": "restore", "step": gap_index, "recovered": true});
  }
  var recovered_order: any = py.sorted(recovered_events, {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any});
  return {"recovered_events": recovered_order, "propagation_order": py.iter(recovered_order).map((event: any) => py.toStr(py.get(event, "id", ""))), "broken_chains_fixed": py.len(gaps), "synchronization_restored": true, "bounded": true};
}
