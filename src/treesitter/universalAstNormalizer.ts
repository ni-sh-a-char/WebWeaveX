/**
 * Converted from Python: core/treesitter/universal_ast_normalizer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_AST_NODES: any = 10000;
export function normalizeAst(raw_nodes: any, language: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var i: any;
  var node: any;
  for ([i, node] of py.enumerate(py.slice(raw_nodes, null, MAX_AST_NODES))) {
    var node_id: any = `${py.toStr(language)}_${py.toStr(i)}`;
    py.listAppend(nodes, {"id": node_id, "type": py.get(node, "type"), "language": language});
    var parent: any = py.get(node, "parent");
    if ((parent !== null && parent !== undefined)) {
      py.listAppend(edges, {"from": parent, "to": node_id, "relation": "ast_edge"});
    }
  }
  return {"nodes": nodes, "edges": edges, "language": language, "bounded": true};
}
