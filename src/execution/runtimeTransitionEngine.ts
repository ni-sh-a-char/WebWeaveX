/**
 * Converted from Python: core/execution/runtime_transition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _VALID_TRANSITIONS: any = {"idle": ["queued", "simulating"], "queued": ["executing", "rolled_back"], "executing": ["committed", "rolled_back", "failed"], "simulating": ["idle"], "committed": ["idle"], "rolled_back": ["idle"], "failed": ["recovering", "idle"], "recovering": ["idle"]};
export function applyRuntimeTransition(state: any, event: any): any {
  var current: any = (py.contains(_VALID_TRANSITIONS, state) ? state : "idle");
  var targets: any = py.get(_VALID_TRANSITIONS, current, ["idle"]);
  if ((py.eq(event, "enqueue") && py.contains(targets, "queued"))) {
    var next_state: any = "queued";
  } else if ((py.eq(event, "execute") && py.contains(targets, "executing"))) {
    next_state = "executing";
  } else if ((py.eq(event, "commit") && py.contains(targets, "committed"))) {
    next_state = "committed";
  } else if ((py.eq(event, "rollback") && py.contains(targets, "rolled_back"))) {
    next_state = "rolled_back";
  } else if ((py.eq(event, "simulate") && py.contains(targets, "simulating"))) {
    next_state = "simulating";
  } else if ((py.eq(event, "fail") && py.contains(targets, "failed"))) {
    next_state = "failed";
  } else if ((py.eq(event, "recover") && py.contains(targets, "recovering"))) {
    next_state = "recovering";
  } else {
    next_state = (py.truthy(targets) ? py.at(targets, 0) : "idle");
  }
  return {"from": current, "to": next_state, "event": event, "valid": py.contains(_VALID_TRANSITIONS, next_state), "bounded": true};
}
