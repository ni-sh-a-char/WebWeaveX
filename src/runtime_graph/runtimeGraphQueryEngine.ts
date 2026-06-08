/**
 * Converted from Python: core/runtime_graph/runtime_graph_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_RESULTS: any = 1000;
export function queryRuntimeGraph(graph: any, query: any): any {
  var nodes: any = [...py.iter(py.or2(py.get(graph, "nodes", []), () => ([])))];
  var node_type: any = py.strip(py.toStr(py.get(query, "type", "")));
  var results: any[] = [];
  var node: any;
  for (node of py.iter(nodes)) {
    if (py.truthy(node_type)) {
      if (!py.eq(py.toStr(py.get(node, "type", "")), node_type)) {
        continue;
      }
    }
    py.listAppend(results, node);
    if ((py.len(results) >= MAX_RESULTS)) {
      break;
    }
  }
  return {"results": results, "count": py.len(results), "bounded": true};
}
