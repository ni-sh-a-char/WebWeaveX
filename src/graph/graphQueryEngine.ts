/**
 * Converted from Python: core/graph/graph_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryNodes(graph: any, node: any = ""): any {
  var nodes: any = (((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map))) ? py.get(graph, "nodes", []) : []);
  if (!py.truthy(node)) {
    return py.iter(nodes).filter((n: any) => ((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map)))).map((n: any) => n);
  }
  return py.iter(nodes).filter((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.eq(py.get(n, "id"), node))).map((n: any) => n);
}
export function queryEdges(graph: any, node: any = ""): any {
  var edges: any = (((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map))) ? py.get(graph, "edges", []) : []);
  if (!py.truthy(node)) {
    return py.iter(edges).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => e);
  }
  return py.iter(edges).filter((e: any) => (((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && (py.eq(py.get(e, "from"), node) || py.eq(py.get(e, "to"), node)))).map((e: any) => e);
}
