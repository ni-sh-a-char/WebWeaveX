/**
 * Converted from Python: core/causality/runtime_sequence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeSequence(events: any): any {
  var ordered: any = py.sorted(events, {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any});
  return {"sequence": py.enumerate(py.slice(ordered, null, 10000)).map(([index, event]: any) => ({"id": py.toStr(py.get(event, "id", "")), "runtime": py.toStr(py.get(event, "runtime", "")), "type": py.toStr(py.get(event, "type", "")), "step": py.toInt(py.get(event, "step", index))})), "length": py.len(ordered), "bounded": true};
}
