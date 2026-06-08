/**
 * Converted from Python: core/execution_physics/semantic_execution_physics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_PRESSURE: any = 100000;
export let STABLE_THRESHOLD: any = 1000;
export function computeExecutionPhysics(runtime_ir: any): any {
  var transitions: any = [...py.iter(py.get(runtime_ir, "transitions", []))];
  var events: any = [...py.iter(py.get(runtime_ir, "events", []))];
  var pressure: any = py.min([py.add(py.len(transitions), py.len(events)), MAX_PRESSURE]);
  var state: any = (py.lt(pressure, STABLE_THRESHOLD) ? "stable" : "unstable");
  return {"execution_pressure": pressure, "physics_state": state, "bounded": true};
}
