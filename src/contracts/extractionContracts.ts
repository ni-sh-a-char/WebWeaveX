/**
 * Converted from Python: core/contracts/extraction_contracts.py
 * @generated — WebWeaveX python→javascript library port
 */


export class ExtractionRequest {
  declare kind: any;
  declare target: any;
  declare authenticated: any;
  declare options: any;
  constructor(kind: any, target: any, authenticated: any = false, options: any = {}) {
    this.kind = kind;
    this.target = target;
    this.authenticated = authenticated;
    this.options = options;
  }
}
export class ExtractionResult {
  declare kind: any;
  declare payload: any;
  declare graph_nodes: any;
  declare graph_edges: any;
  declare deterministic_hash: any;
  constructor(kind: any, payload: any, graph_nodes: any = [], graph_edges: any = [], deterministic_hash: any = "") {
    this.kind = kind;
    this.payload = payload;
    this.graph_nodes = graph_nodes;
    this.graph_edges = graph_edges;
    this.deterministic_hash = deterministic_hash;
  }
  to_dict(): any {
    return {"kind": this.kind, "payload": this.payload, "graph_nodes": this.graph_nodes, "graph_edges": this.graph_edges, "deterministic_hash": this.deterministic_hash, "bounded": true};
  }
}
