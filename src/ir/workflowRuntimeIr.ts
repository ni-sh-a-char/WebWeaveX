/**
 * Converted from Python: core/ir/workflow_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileWorkflowRuntimeIr(workflow: any): any {
  return {"ir": "workflow_runtime", "objective": py.get(workflow, "objective", {}), "plan": py.get(workflow, "plan", {}), "execution": py.get(workflow, "execution", {}), "state": py.get(workflow, "state", {}), "workflow_graph": py.get(workflow, "workflow_graph", {}), "dependencies": py.get(workflow, "dependencies", {}), "federation": py.get(workflow, "federation", {}), "semantic_alignment": py.get(workflow, "semantic_alignment", {}), "recovery": py.get(workflow, "recovery", {}), "bounded": true};
}
export function workflowRuntimeIrToGraph(workflow_ir: any): any {
  var graph: any = py.get(workflow_ir, "workflow_graph", {});
  var nodes: any = [...py.iter(py.get(graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "workflow:root", "type": "workflow"}];
  }
  return {"ir": "workflow_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
