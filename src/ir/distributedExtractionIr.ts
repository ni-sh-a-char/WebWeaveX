/**
 * Converted from Python: core/ir/distributed_extraction_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileDistributedExtractionIr(workers: any, queue: any, topology: any, identities: any, streams: any, adaptive: any, checkpoint: any, recovery: any): any {
  return {"ir": "distributed_extraction", "workers": py.get(workers, "workers", workers), "queues": py.get(queue, "queue", queue), "runtime_topology": py.get(topology, "topology", topology), "identities": identities, "streams": streams, "adaptive_runtimes": adaptive, "checkpoints": checkpoint, "recovery_state": recovery, "bounded": true};
}
export function distributedExtractionIrToGraph(distributed_ir: any): any {
  var workers: any = py.get(distributed_ir, "workers", []);
  var nodes: any[] = [];
  var edges: any[] = [];
  var worker: any;
  for (worker of py.iter(workers)) {
    if (((worker !== null && typeof worker === "object" && !Array.isArray(worker) && !(worker instanceof Set) && !(worker instanceof Map)))) {
      var node_id: any = py.toStr(py.get(worker, "worker_id", ""));
      py.listAppend(nodes, {"id": node_id, "type": "worker", "name": node_id});
    }
  }
  var index: any;
  for (index = 0; index < py.sub(py.len(nodes), 1); index++) {
    py.listAppend(edges, {"from": py.at(py.at(nodes, index), "id"), "to": py.at(py.at(nodes, py.add(index, 1)), "id"), "relation": "cluster_next"});
  }
  return {"ir": "distributed_extraction_graph", "nodes": nodes, "edges": edges, "bounded": true};
}
