/**
 * Converted from Python: core/runtime/runtime_state_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_PROPAGATION_DEPTH: any = 50;
export function propagateRuntimeState(transitions: any): any {
  var states: Set<any> = new Set();
  var t: any;
  for (t of py.iter(py.slice(transitions, null, MAX_PROPAGATION_DEPTH))) {
    py.setAdd(states, py.at(t, "from"));
    py.setAdd(states, py.at(t, "to"));
  }
  return {"reachable_states": py.sorted(states), "state_count": py.len(states), "bounded": true};
}
