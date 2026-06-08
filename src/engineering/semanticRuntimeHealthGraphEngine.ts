/**
 * Converted from Python: core/engineering/semantic_runtime_health_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_HEALTH_NODES: any = 10000;
export function buildRuntimeHealthGraph(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var nodes: any = py.get(topology, "nodes", []);
  var health_nodes: any[] = [];
  var node: any;
  for (node of py.iter(py.slice(nodes, null, MAX_HEALTH_NODES))) {
    py.listAppend(health_nodes, {"id": py.get(node, "id"), "status": "healthy"});
  }
  return {"health_nodes": health_nodes, "bounded": true};
}
