/**
 * Converted from Python: core/typed_ir/typed_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { propagateRuntimeState } from "../runtime/runtimeStatePropagationEngine.js";
import { ExecutionState, RuntimeTransition } from "./schemaTypes.js";

export function compileTypedRuntimeIr(transitions: any): any {
  var typed_transitions: any[] = [];
  var t: any;
  for (t of py.iter(transitions)) {
    py.listAppend(typed_transitions, new RuntimeTransition(py.toStr(py.get(t, "from", py.get(t, "from_state", ""))), py.toStr(py.get(t, "to", py.get(t, "to_state", ""))), py.toStr(py.get(t, "transition_type", py.get(t, "type", "step")))));
  }
  var propagation: any = propagateRuntimeState(py.iter(typed_transitions).map((tr: any) => ({"from": tr.from_state, "to": tr.to_state})));
  var states: any = py.iter(py.get(propagation, "reachable_states", [])).map((s: any) => new ExecutionState(s, "reachable"));
  return {"transitions": typed_transitions, "states": states, "propagation": propagation, "typed": true, "deterministic": true};
}
export { ExecutionState, RuntimeTransition, propagateRuntimeState };
