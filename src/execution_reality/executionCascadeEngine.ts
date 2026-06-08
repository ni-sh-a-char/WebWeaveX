/**
 * Converted from Python: core/execution_reality/execution_cascade_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CASCADE: any = 10000;
export function traceExecutionCascade(transitions: any): any {
  var ordered: any = py.slice(py.sorted(transitions, {key: ((x: any) => [py.toStr(py.get(x, "from")), py.toStr(py.get(x, "to"))]) as (item: any) => any}), null, MAX_CASCADE);
  var cascade: any = py.iter(ordered).map((t: any) => ({"from": py.get(t, "from"), "to": py.get(t, "to")}));
  return {"cascade": cascade, "cascade_length": py.len(cascade), "bounded": true};
}
