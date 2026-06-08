/**
 * Converted from Python: core/ir/application_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileApplicationRuntimeIr(cognition: any, recovery: any): any {
  return {"ir": "application_runtime", "application_states": [py.get(cognition, "application_state", {})], "workflows": py.get(cognition, "workflow", {}), "forms": py.get(cognition, "forms", {}), "action_graphs": py.get(cognition, "action_graph", {}), "dashboard_runtime": py.get(cognition, "dashboard", {}), "navigation_semantics": py.get(cognition, "navigation", {}), "objectives": py.get(py.get(cognition, "memory", {}), "objectives", []), "recovery_state": recovery, "execution": py.get(cognition, "execution", {}), "bounded": true};
}
export function applicationRuntimeIrToGraph(application_ir: any): any {
  var workflow: any = py.get(application_ir, "workflows", {});
  var nodes: any = [...py.iter(py.get(workflow, "nodes", []))];
  var edges: any = [...py.iter(py.get(workflow, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "application:root", "type": "application"}];
  }
  return {"ir": "application_runtime_graph", "nodes": nodes, "edges": edges, "bounded": true};
}
