/**
 * Converted from Python: core/application/application_transition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildApplicationTransitions(states: any): any {
  var transitions: any[] = [];
  var index: any;
  for (index = 0; index < py.sub(py.len(states), 1); index++) {
    var src: any = py.at(states, index);
    var dst: any = py.at(states, py.add(index, 1));
    py.listAppend(transitions, {"from": py.toStr(py.get(src, "route", "")), "to": py.toStr(py.get(dst, "route", "")), "relation": "transition", "order": index});
  }
  return py.slice(transitions, null, 10000);
}
