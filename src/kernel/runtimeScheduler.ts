/**
 * Converted from Python: core/kernel/runtime_scheduler.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function scheduleKernelPhases(phases: any, tick: any = 0): any {
  var scheduled: any = py.enumerate(phases).map(([index, phase]: any) => ({"phase": phase, "tick": py.add(tick, index), "priority": index}));
  return {"scheduled": py.sorted(scheduled, {key: ((item: any) => py.at(item, "priority")) as (item: any) => any}), "deterministic": true, "bounded": true};
}
