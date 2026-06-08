/**
 * Converted from Python: core/execution_reality/semantic_execution_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_PRESSURE: any = 100000;
export function computeExecutionPressure(runtime_ir: any): any {
  var transitions: any = [...py.iter(py.get(runtime_ir, "transitions", []))];
  var event_stream: any = py.get(runtime_ir, "event_stream", {});
  var events: any = [...py.iter((((event_stream !== null && typeof event_stream === "object" && !Array.isArray(event_stream) && !(event_stream instanceof Set) && !(event_stream instanceof Map))) ? py.get(event_stream, "events", []) : []))];
  var pressure_score: any = py.min([py.add(py.len(transitions), py.len(events)), MAX_PRESSURE]);
  return {"pressure_score": pressure_score, "bounded": true};
}
