/**
 * Converted from Python: core/ir/runtime_memory_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileRuntimeMemoryIr(memory_payload: any): any {
  return {"ir": "runtime_memory", "memory_graphs": py.get(memory_payload, "graph", {}), "semantic_indexes": py.get(memory_payload, "index", {}), "lineage": py.get(memory_payload, "lineage", {}), "runtime_history": py.get(memory_payload, "runtime", {}), "distributed_memory": py.get(memory_payload, "distributed", {}), "knowledge": py.get(memory_payload, "knowledge", {}), "semantic": py.get(memory_payload, "semantic", {}), "bounded": true};
}
export function runtimeMemoryIrToGraph(memory_ir: any): any {
  var graph: any = py.get(memory_ir, "memory_graphs", {});
  var nodes: any = [...py.iter(py.get(graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "memory:root", "type": "memory"}];
  }
  return {"ir": "runtime_memory_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
