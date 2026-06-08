/**
 * Converted from Python: core/execution_physics/runtime_energy_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_PROPAGATION: any = 10000;
export function propagateRuntimeEnergy(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var edges: any = [...py.iter(py.get(topology, "edges", []))];
  var propagation: any[] = [];
  var edge: any;
  for (edge of py.iter(py.slice(edges, null, MAX_PROPAGATION))) {
    py.listAppend(propagation, {"from": py.get(edge, "from"), "to": py.get(edge, "to"), "energy_transfer": 1});
  }
  return {"energy_propagation": py.sorted(propagation, {key: ((x: any) => [py.toStr(py.at(x, "from")), py.toStr(py.at(x, "to"))]) as (item: any) => any}), "bounded": true};
}
