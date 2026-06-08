/**
 * Converted from Python: core/runtime/runtime_simulation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_SIMULATION_STEPS: any = 100;
export function simulateRuntimeExecution(transitions: any): any {
  var visited: any[] = [];
  var current: any = null;
  var t: any;
  for (t of py.iter(py.slice(transitions, null, MAX_SIMULATION_STEPS))) {
    current = py.at(t, "to");
    py.listAppend(visited, current);
  }
  return {"visited_states": visited, "final_state": current, "steps": py.len(visited), "bounded": true};
}
