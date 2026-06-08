/**
 * Converted from Python: core/runtime/runtime_transition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";
import { RuntimeStateMachine } from "./runtimeStateMachineEngine.js";

export function applyRuntimeTransitions(states: any, evidence: any = null): any {
  var sm: any = new RuntimeStateMachine();
  var transitions: any[] = [];
  var nxt: any;
  for (nxt of py.iter(states)) {
    var t: any = sm.transition(nxt, evidence);
    py.listAppend(transitions, {"previous": t.previous, "current": t.current, "valid": t.valid, "evidence": t.evidence});
  }
  return {"final_state": sm.state, "transitions": transitions, "deterministic": true};
}
export { RuntimeStateMachine };
