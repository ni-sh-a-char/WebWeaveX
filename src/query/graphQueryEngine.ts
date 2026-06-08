/**
 * Converted from Python: core/query/graph_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { queryEdges, queryNodes } from "../agents/graphQueryEngine.js";
import { compileSemanticGraphIr } from "../ir/semanticGraphIr.js";

export function queryGraph(graph: any, node: any = ""): any {
  var ir: any = compileSemanticGraphIr(graph);
  return {"ir": ir, "nodes": queryNodes(graph, node), "edges": queryEdges(graph, node), "explainable": true, "bounded": true};
}
export { compileSemanticGraphIr, queryEdges, queryNodes };
