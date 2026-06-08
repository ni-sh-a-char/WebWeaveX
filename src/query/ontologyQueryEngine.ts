/**
 * Converted from Python: core/query/ontology_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileKnowledgeIr } from "../ir/knowledgeIr.js";

export function queryKnowledge(entities: any, edges: any): any {
  var ir: any = compileKnowledgeIr(entities, edges);
  return {"ir": ir, "relations": py.get(ir, "relations", []), "contradictions": py.get(ir, "contradictions", []), "explainable": true};
}
export { compileKnowledgeIr };
