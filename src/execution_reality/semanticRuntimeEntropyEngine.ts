/**
 * Converted from Python: core/execution_reality/semantic_runtime_entropy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeRuntimeEntropy(runtime_ir: any): any {
  var transitions: any = py.get(runtime_ir, "transitions", []);
  var unique_states: Set<any> = new Set();
  var transition: any;
  for (transition of py.iter(transitions)) {
    py.setAdd(unique_states, py.toStr(py.get(transition, "from")));
    py.setAdd(unique_states, py.toStr(py.get(transition, "to")));
  }
  var entropy_score: any = py.len(unique_states);
  return {"entropy_score": entropy_score};
}
