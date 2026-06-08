/**
 * Converted from Python: core/database/semantic_graph_database.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticGraphDatabase {
  declare nodes: any;
  declare edges: any;
  constructor() {
    this.nodes = {};
    this.edges = [];
  }
  insert_node(node: any): any {
    var node_id: any = py.get(node, "id");
    if (!py.truthy(node_id)) {
      return;
    }
    py.setItem(this.nodes, node_id, node);
  }
  insert_edge(edge: any): any {
    py.listAppend(this.edges, edge);
  }
  query_node(node_id: any): any {
    return py.get(this.nodes, node_id, {});
  }
  stats(): any {
    return {"nodes": py.len(this.nodes), "edges": py.len(this.edges)};
  }
}
