/**
 * Converted from Python: core/workflows/workflow_transition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWorkflowTransitions(execution: any): any {
  var transitions: any[] = [];
  var executed: any = [...py.iter(py.get(execution, "executed", []))];
  var index: any;
  for (index = 1; index < py.len(executed); index++) {
    py.listAppend(transitions, {"from": py.toStr(py.get(py.at(executed, py.sub(index, 1)), "step_id", "")), "to": py.toStr(py.get(py.at(executed, index), "step_id", "")), "relation": "transitions"});
  }
  return transitions;
}
