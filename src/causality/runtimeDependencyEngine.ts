/**
 * Converted from Python: core/causality/runtime_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeDependencies(events: any, propagation: any): any {
  var dependencies: any[] = [];
  var consumers: any[] = [];
  var sync_chains: any[] = [];
  var runtimes_seen: any[] = [];
  var event: any;
  for (event of py.iter(py.sorted(events, {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any}))) {
    var runtime: any = py.toStr(py.get(event, "runtime", ""));
    if ((py.truthy(runtime) && !py.contains(runtimes_seen, runtime))) {
      if (py.truthy(runtimes_seen)) {
        py.listAppend(dependencies, {"from": py.at(runtimes_seen, (-1)), "to": runtime, "relation": "depends_on"});
      }
      py.listAppend(runtimes_seen, runtime);
      py.listAppend(consumers, {"runtime": runtime, "event_id": py.toStr(py.get(event, "id", ""))});
    }
  }
  var handoff: any;
  for (handoff of py.iter(py.slice(py.get(propagation, "handoffs", []), null, 5000))) {
    py.listAppend(sync_chains, {"from": py.get(handoff, "from", ""), "to": py.get(handoff, "to", ""), "workflow_id": py.get(handoff, "workflow_id", "")});
  }
  return {"dependencies": dependencies, "consumers": consumers, "synchronization_chains": sync_chains, "causal_relationships": dependencies, "bounded": true};
}
