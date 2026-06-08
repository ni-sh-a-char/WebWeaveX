/**
 * Converted from Python: core/execution_physics/distributed_runtime_gravity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_GRAVITY: any = 100000;
export function computeRuntimeGravity(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var node_count: any = py.len(py.get(topology, "nodes", []));
  var edge_count: any = py.len(py.get(topology, "edges", []));
  var gravity: any = py.min([py.add(node_count, edge_count), MAX_GRAVITY]);
  return {"gravity": gravity, "node_count": node_count, "bounded": true};
}
