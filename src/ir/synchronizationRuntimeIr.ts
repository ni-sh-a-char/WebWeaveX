/**
 * Converted from Python: core/ir/synchronization_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileSynchronizationRuntimeIr(sync: any): any {
  return {"ir": "synchronization_runtime", "snapshot": py.get(sync, "snapshot", {}), "delta": py.get(sync, "delta", {}), "history": py.get(sync, "history", {}), "timeline": py.get(sync, "timeline", {}), "convergence": py.get(sync, "convergence", {}), "synchronization": py.get(sync, "synchronization", {}), "replication": py.get(sync, "replication", {}), "continuity": py.get(sync, "continuity", {}), "state_graph": py.get(sync, "state_graph", {}), "consistency": py.get(sync, "consistency", {}), "bounded": true};
}
export function synchronizationRuntimeIrToGraph(sync_ir: any): any {
  var graph: any = py.get(sync_ir, "state_graph", {});
  var nodes: any = [...py.iter(py.get(graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "sync:root", "type": "synchronization"}];
  }
  return {"ir": "synchronization_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
