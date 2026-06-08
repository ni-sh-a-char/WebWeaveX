/**
 * Converted from Python: core/ir/causal_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileCausalRuntimeIr(cognition: any): any {
  return {"ir": "causal_runtime", "causal_graphs": py.get(cognition, "causal_graph", {}), "timelines": py.get(cognition, "timeline", {}), "event_chains": py.get(cognition, "event_chain", {}), "propagation_maps": py.get(cognition, "propagation", {}), "distributed_synchronization": py.get(cognition, "distributed", {}), "runtime_dependencies": py.get(cognition, "dependencies", {}), "alignment": py.get(cognition, "alignment", {}), "bridges": {"browser_native": py.get(cognition, "browser_bridge", {}), "electron_terminal": py.get(cognition, "electron_bridge", {})}, "recovery_state": py.get(cognition, "recovery", {}), "bounded": true};
}
export function causalRuntimeIrToGraph(causal_ir: any): any {
  var graph: any = py.get(causal_ir, "causal_graphs", {});
  var nodes: any = [...py.iter(py.get(graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "causality:root", "type": "causality"}];
  }
  var timeline: any = py.get(causal_ir, "timelines", {});
  var entry: any;
  for (entry of py.iter(py.slice(py.get(timeline, "timeline", []), null, 5000))) {
    py.listAppend(nodes, {"id": py.toStr(py.get(entry, "event_id", "")), "type": "timeline_event", "runtime": py.toStr(py.get(entry, "runtime", ""))});
  }
  return {"ir": "causal_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
