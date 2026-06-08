/**
 * Converted from Python: core/runtime/semantic_execution_graph.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export class SemanticExecutionGraph {
  declare max_nodes: any;
  declare nodes: any;
  declare edges: any;
  constructor(max_nodes: any = 500) {
    this.max_nodes = max_nodes;
    this.nodes = [];
    this.edges = [];
  }
  add_node(node_id: any, kind: any, metadata: any = null): any {
    if ((py.len(this.nodes) >= this.max_nodes)) {
      return false;
    }
    py.listAppend(this.nodes, {"id": node_id, "kind": kind, "metadata": py.or2(metadata, () => ({}))});
    return true;
  }
  add_edge(fr: any, to: any, evidence: any = null): any {
    if ((py.len(this.edges) >= this.max_nodes)) {
      return false;
    }
    py.listAppend(this.edges, {"from": fr, "to": to, "evidence": py.or2(evidence, () => ([])), "metadata": {}});
    return true;
  }
  to_dict(): any {
    return {"nodes": this.nodes, "edges": this.edges, "bounded": (py.len(this.nodes) <= this.max_nodes)};
  }
}
