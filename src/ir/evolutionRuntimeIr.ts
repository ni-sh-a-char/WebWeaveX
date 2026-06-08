/**
 * Converted from Python: core/ir/evolution_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileEvolutionRuntimeIr(evolution: any): any {
  return {"ir": "evolution_runtime", "evolution": py.get(evolution, "evolution", {}), "selector": py.get(evolution, "selector", {}), "workflow": py.get(evolution, "workflow", {}), "semantic": py.get(evolution, "semantic", {}), "topology": py.get(evolution, "topology", {}), "strategy": py.get(evolution, "strategy", {}), "repairs": py.get(evolution, "repairs", {}), "optimization": py.get(evolution, "optimization", {}), "patterns": py.get(evolution, "patterns", {}), "lineage": py.get(evolution, "lineage", []), "graph": py.get(evolution, "graph", {}), "policy": py.get(evolution, "policy", {}), "bounded": true};
}
export function evolutionRuntimeIrToGraph(evolution_ir: any): any {
  var graph: any = py.get(evolution_ir, "graph", {});
  var nodes: any = [...py.iter(py.get(graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "evolution:root", "type": "evolution"}];
  }
  return {"ir": "evolution_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
