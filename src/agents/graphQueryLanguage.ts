/**
 * Converted from Python: core/agents/graph_query_language.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function runGql(graph: any, query: any): any {
  var q: any = String(py.strip(py.or2(query, () => ("")))).toLowerCase();
  if (py.eq(q, "nodes")) {
    return py.get(graph, "nodes", []);
  }
  if (py.eq(q, "edges")) {
    return py.get(graph, "edges", []);
  }
  return [];
}
