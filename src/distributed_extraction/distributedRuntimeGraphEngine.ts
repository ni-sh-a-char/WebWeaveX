/**
 * Converted from Python: core/distributed_extraction/distributed_runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDistributedRuntimeGraph(workers: any, topology: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var worker: any;
  for (worker of py.iter(workers)) {
    var worker_id: any = py.toStr(py.get(worker, "worker_id", ""));
    py.listAppend(nodes, {"id": worker_id, "type": "worker", "status": py.get(worker, "status", "idle")});
  }
  var topology_nodes: any = py.get(topology, "nodes", []);
  var node: any;
  for (node of py.iter(topology_nodes)) {
    py.listAppend(nodes, {"id": py.toStr(py.get(node, "id", "")), "type": py.get(node, "type", "runtime")});
  }
  var index: any;
  for (index = 0; index < py.sub(py.len(workers), 1); index++) {
    py.listAppend(edges, {"from": py.toStr(py.get(py.at(workers, index), "worker_id", "")), "to": py.toStr(py.get(py.at(workers, py.add(index, 1)), "worker_id", "")), "relation": "worker_next"});
  }
  return {"ir": "distributed_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
