/**
 * Converted from Python: core/causal_intelligence/execution_timing_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TIMING: any = 10000;
export function analyzeExecutionTiming(runtime_ir: any): any {
  var event_stream: any = py.get(runtime_ir, "event_stream", {});
  var events: any = py.sorted([...py.iter((((event_stream !== null && typeof event_stream === "object" && !Array.isArray(event_stream) && !(event_stream instanceof Set) && !(event_stream instanceof Map))) ? py.get(event_stream, "events", []) : []))], {key: ((x: any) => [py.get(x, "timestamp", 0), py.toStr(py.get(x, "id"))]) as (item: any) => any});
  return {"timing_sequence": py.iter(py.slice(events, null, MAX_TIMING)).map((e: any) => py.toStr(py.get(e, "id"))), "bounded": true};
}
