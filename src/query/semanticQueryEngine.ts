/**
 * Converted from Python: core/query/semantic_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileSemanticQueryIr } from "../ir/semanticQueryIr.js";
import { queryRepository } from "./repositoryQueryEngine.js";
import { queryDocuments } from "./documentQueryEngine.js";
import { queryGraph } from "./graphQueryEngine.js";
import { queryKnowledge } from "./ontologyQueryEngine.js";

export function querySemantics(query_type: any, payload: any): any {
  var dispatch: any = {"repository": () => queryRepository(py.get(payload, "source", ""), py.get(payload, "path", "")), "document": () => queryDocuments(py.get(payload, "text", "")), "graph": () => queryGraph(py.get(payload, "graph", {})), "knowledge": () => queryKnowledge(py.get(payload, "entities", []), py.get(payload, "edges", []))};
  var fn: any = py.get(dispatch, query_type);
  if (!py.truthy(fn)) {
    return compileSemanticQueryIr(query_type, "", {"error": "unknown_query_type"});
  }
  var result: any = fn();
  return compileSemanticQueryIr(query_type, py.slice(py.toStr(payload), null, 80), result);
}
export { compileSemanticQueryIr, queryDocuments, queryGraph, queryKnowledge, queryRepository };
