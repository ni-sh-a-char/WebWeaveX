/**
 * Converted from Python: core/ir/semantic_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileSemanticRuntimeIr(cognition: any): any {
  return {"ir": "semantic_runtime", "ontology": py.get(cognition, "ontology", {}), "entities": py.get(cognition, "entities", {}), "semantic_graph": py.get(cognition, "semantic_graph", {}), "domain": py.get(cognition, "domain", {}), "ui_semantics": py.get(cognition, "ui", {}), "table_semantics": py.get(cognition, "tables", {}), "document_semantics": py.get(cognition, "document", {}), "repository_semantics": py.get(cognition, "repository", {}), "application_semantics": py.get(cognition, "application", {}), "causality_semantics": py.get(cognition, "causality", {}), "workflow_semantics": py.get(cognition, "workflow", {}), "alignment": py.get(cognition, "alignment", {}), "bounded": true};
}
export function semanticRuntimeIrToGraph(semantic_ir: any): any {
  var graph: any = py.get(semantic_ir, "semantic_graph", {});
  var nodes: any = [...py.iter(py.get(graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  var ontology: any = py.get(semantic_ir, "ontology", {});
  if (py.truthy(py.get(ontology, "primary_domain"))) {
    py.listAppend(nodes, {"id": `domain:${py.toStr(py.at(ontology, "primary_domain"))}`, "type": "domain"});
  }
  if (!py.truthy(nodes)) {
    nodes = [{"id": "semantic:root", "type": "semantic"}];
  }
  return {"ir": "semantic_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
