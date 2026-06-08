/**
 * Converted from Python: core/agents/graph_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryNodes(graph: any, node: any = ""): any {
  var nodes: any = py.get(graph, "nodes", []);
  if (!py.truthy(node)) {
    return nodes;
  }
  return py.iter(nodes).filter((n: any) => py.contains(py.toStr(py.get(n, "id", "")), node)).map((n: any) => n);
}
export function queryEdges(graph: any, node: any = ""): any {
  var edges: any = py.get(graph, "edges", []);
  if (!py.truthy(node)) {
    return edges;
  }
  return py.iter(edges).filter((e: any) => (py.contains(py.get(e, "from", ""), node) || py.contains(py.get(e, "to", ""), node))).map((e: any) => e);
}
export function queryDependencies(result: any): any {
  return py.get(result, "dependencies", {});
}
export function queryServices(result: any): any {
  return py.get(py.get(result, "repository", {}), "services", []);
}
