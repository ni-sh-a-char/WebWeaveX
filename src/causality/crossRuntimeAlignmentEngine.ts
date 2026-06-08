/**
 * Converted from Python: core/causality/cross_runtime_alignment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let RUNTIME_ORDER: any = ["browser", "application", "electron", "desktop", "terminal", "vm", "remote", "distributed"];
export function alignCrossRuntimeEvents(events: any): any {
  var buckets: any = Object.fromEntries(py.iter(RUNTIME_ORDER).map((runtime: any) => ([runtime, []] as [any, any])));
  var event: any;
  for (event of py.iter(py.slice(events, null, 20000))) {
    var runtime: any = String(py.toStr(py.get(event, "runtime", "browser"))).toLowerCase();
    if (!py.contains(buckets, runtime)) {
      py.setItem(buckets, runtime, []);
    }
    py.listAppend(py.at(buckets, runtime), event);
  }
  var aligned: any[] = [];
  var step: any = 0;
  for (runtime of py.iter(RUNTIME_ORDER)) {
    for (event of py.iter(py.sorted(py.get(buckets, runtime, []), {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any}))) {
      py.listAppend(aligned, {...(event), "aligned_step": step, "aligned_runtime": runtime});
      step = py.add(step, 1);
    }
  }
  var correlations: any[] = [];
  var index: any;
  for (index = 1; index < py.len(aligned); index++) {
    var prev: any = py.at(aligned, py.sub(index, 1));
    var curr: any = py.at(aligned, index);
    py.listAppend(correlations, {"from_runtime": py.get(prev, "runtime", ""), "to_runtime": py.get(curr, "runtime", ""), "from_event": py.get(prev, "id", ""), "to_event": py.get(curr, "id", ""), "correlation_id": `corr:${py.toStr(index)}`});
  }
  return {"aligned_events": aligned, "correlations": correlations, "runtime_count": py.len(py.toSet(py.iter(aligned).map((e: any) => py.get(e, "runtime")))), "bounded": true};
}
