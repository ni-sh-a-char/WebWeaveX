/**
 * Converted from Python: core/runtime/runtime_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";
import { RuntimeStateMachine } from "./runtimeStateMachineEngine.js";

export function recoverRuntime(failed_state: any, evidence: any = null): any {
  var sm: any = new RuntimeStateMachine();
  if (!py.eq(failed_state, "initialized")) {
    sm.transition(failed_state, evidence);
  }
  sm.transition("retrying", py.or2(evidence, () => (["recovery"])));
  sm.transition("running", py.or2(evidence, () => (["recovery"])));
  return {"recovered_state": sm.state, "transitions": py.len(sm.history), "deterministic": true};
}
export { RuntimeStateMachine };
