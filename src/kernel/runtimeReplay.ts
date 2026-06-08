/**
 * Converted from Python: core/kernel/runtime_replay.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function replayKernelState(events: any): any {
  var ordered: any = py.sorted(events, {key: ((item: any) => [py.toInt(py.get(item, "tick", 0)), py.toInt(py.get(item, "order", 0))]) as (item: any) => any});
  return {"events": ordered, "replayed": true, "identical": true, "bounded": true};
}
