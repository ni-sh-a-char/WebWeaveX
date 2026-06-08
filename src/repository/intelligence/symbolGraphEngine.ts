/**
 * Converted from Python: core/repository/intelligence/symbol_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildSymbolGraph(ast_data: any): any {
  var nodes: any = py.sorted(py.toSet(py.get(ast_data, "symbols", [])));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1))}));
  return {"nodes": nodes, "edges": edges};
}
