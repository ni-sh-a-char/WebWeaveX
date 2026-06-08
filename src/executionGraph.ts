/**
 * Converted from Python: core/execution_graph.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";
import { MAX_EDGES as MAX_EDGES_V3 } from "./graph/graphReconstructionEngine.js";
import { MAX_NODES, reconstructGraph } from "./graph/graphReconstructionEngine.js";

export let MAX_EDGES: any = 500;
export function buildExecutionGraph(system_graph: any, max_edges: any = MAX_EDGES, max_nodes: any = MAX_NODES): any {
  return reconstructGraph(system_graph, max_edges, max_nodes);
}
export function inferExecutionOrder(system_graph: any): any {
  var graph: any = buildExecutionGraph(system_graph);
  return py.iter(py.at(graph, "nodes")).map((n: any) => py.at(n, "id"));
}
export function buildExecutionGraphV3(system_graph: any): any {
  return reconstructGraph(system_graph, MAX_EDGES_V3, MAX_NODES);
}
export { MAX_EDGES_V3, MAX_NODES, reconstructGraph };
