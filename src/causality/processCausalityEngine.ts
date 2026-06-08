/**
 * Converted from Python: core/causality/process_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackProcessCausality(processes: any, events: any): any {
  var chains: any[] = [];
  var index: any;
  var process: any;
  for ([index, process] of py.enumerate(py.slice(processes, null, 5000))) {
    var parent: any = py.toStr(py.get(process, "parent", ""));
    py.listAppend(chains, {"process": py.toStr(py.get(process, "name", py.get(process, "pid", `proc:${py.toStr(index)}`))), "parent": parent, "launched_at_step": index, "mutation_event": py.toStr(((index < py.len(events)) ? py.get(py.at(events, index), "id", "") : ""))});
  }
  return {"process_chains": chains, "subprocess_depth": py.max(py.iter(chains).map((c: any) => py.get(c, "launched_at_step", 0)), {dflt: 0, hasDefault: true}), "bounded": true};
}
