/**
 * Converted from Python: core/hypergraph/semantic_hypergraph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_HYPEREDGES: any = 10000;
export function buildSemanticHypergraph(nodes: any, relationships: any): any {
  var hyperedges: any[] = [];
  var rel: any;
  for (rel of py.iter(py.slice(relationships, null, MAX_HYPEREDGES))) {
    var members: any = py.get(rel, "members", []);
    if ((py.len(members) < 2)) {
      continue;
    }
    py.listAppend(hyperedges, {"type": py.get(rel, "type"), "members": py.sorted(members)});
  }
  return {"nodes": nodes, "hyperedges": hyperedges, "bounded": true};
}
