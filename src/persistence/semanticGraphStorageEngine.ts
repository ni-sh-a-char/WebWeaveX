/**
 * Converted from Python: core/persistence/semantic_graph_storage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticGraphStorage {
  declare nodes: any;
  declare edges: any;
  constructor() {
    this.nodes = {};
    this.edges = [];
  }
  add_node(node: any): any {
    py.setItem(this.nodes, py.at(node, "id"), node);
  }
  add_edge(edge: any): any {
    py.listAppend(this.edges, edge);
  }
  snapshot(): any {
    return {"nodes": [...py.iter(py.values(this.nodes))], "edges": this.edges};
  }
}
