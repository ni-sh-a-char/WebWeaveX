/**
 * Converted from Python: core/graph/semantic_symbol_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SYMBOLS: any = 5000;
export function buildSemanticSymbolGraph(symbols: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var i: any;
  var sym: any;
  for ([i, sym] of py.enumerate(py.slice(symbols, null, MAX_SYMBOLS))) {
    var node_id: any = py.at(sym, "name");
    py.listAppend(nodes, {"id": node_id, "kind": "symbol"});
    var refs: any = py.get(sym, "references", []);
    var ref: any;
    for (ref of py.iter(refs)) {
      py.listAppend(edges, {"from": node_id, "to": ref, "relation": "symbol_reference"});
    }
  }
  return {"nodes": nodes, "edges": edges, "bounded": true};
}
