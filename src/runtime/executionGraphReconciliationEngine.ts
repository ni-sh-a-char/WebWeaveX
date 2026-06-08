/**
 * Converted from Python: core/runtime/execution_graph_reconciliation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function reconcileExecutionGraphs(runtime_graph: any, topology_graph: any): any {
  var runtime_nodes: any = py.toSet(py.iter(py.get(runtime_graph, "nodes", [])).map((n: any) => py.at(n, "id")));
  var topology_nodes: any = py.toSet(py.iter(py.get(topology_graph, "nodes", [])).map((n: any) => py.at(n, "id")));
  var overlap: any = py.sorted(py.bitand(runtime_nodes, topology_nodes));
  return {"shared_nodes": overlap, "runtime_only": py.sorted(py.sub(runtime_nodes, topology_nodes)), "topology_only": py.sorted(py.sub(topology_nodes, runtime_nodes)), "consistent": (py.len(overlap) > 0)};
}
