/**
 * Converted from Python: core/causality/workflow_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWorkflowPropagation(aligned: any, dependencies: any): any {
  var events: any = [...py.iter(py.get(aligned, "aligned_events", []))];
  var handoffs: any[] = [];
  var index: any;
  for (index = 1; index < py.len(events); index++) {
    var prev: any = py.at(events, py.sub(index, 1));
    var curr: any = py.at(events, index);
    if (!py.eq(py.get(prev, "runtime"), py.get(curr, "runtime"))) {
      py.listAppend(handoffs, {"from": py.toStr(py.get(prev, "runtime", "")), "to": py.toStr(py.get(curr, "runtime", "")), "step": index, "workflow_id": `wf:${py.toStr(index)}`});
    }
  }
  return {"continuations": handoffs, "handoffs": handoffs, "distributed": [...py.iter(py.get(dependencies, "synchronization_chains", []))], "synchronized_steps": py.iter(events).map((event: any) => py.get(event, "aligned_step", 0)), "bounded": true};
}
