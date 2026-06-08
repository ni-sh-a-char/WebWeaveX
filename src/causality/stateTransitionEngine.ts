/**
 * Converted from Python: core/causality/state_transition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildStateTransitions(events: any): any {
  var transitions: any[] = [];
  var index: any;
  for (index = 1; index < py.len(events); index++) {
    var prev: any = py.at(events, py.sub(index, 1));
    var curr: any = py.at(events, index);
    py.listAppend(transitions, {"from_state": py.toStr(py.get(prev, "state", py.get(prev, "type", ""))), "to_state": py.toStr(py.get(curr, "state", py.get(curr, "type", ""))), "runtime": py.toStr(py.get(curr, "runtime", "")), "step": index});
  }
  return {"transitions": transitions, "count": py.len(transitions), "bounded": true};
}
