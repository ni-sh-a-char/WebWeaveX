/**
 * Converted from Python: core/causal_intelligence/distributed_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_PROPAGATION: any = 10000;
export function propagateDistributedState(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var edges: any = [...py.iter(py.get(topology, "edges", []))];
  var propagation: any[] = [];
  var edge: any;
  for (edge of py.iter(edges)) {
    py.listAppend(propagation, {"source": py.get(edge, "from"), "target": py.get(edge, "to"), "propagates": true});
  }
  return {"propagation_paths": py.slice(py.sorted(propagation, {key: ((x: any) => [py.toStr(py.at(x, "source")), py.toStr(py.at(x, "target"))]) as (item: any) => any}), null, MAX_PROPAGATION), "bounded": true};
}
