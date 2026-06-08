/**
 * Converted from Python: core/world_model/repository_knowledge_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeSymbols } from "./_normalize.js";

export function buildRepositoryKnowledgeGraph(repository_irs: any): any {
  var entities: any[] = [];
  var relationships: any[] = [];
  var ir: any;
  for (ir of py.iter(repository_irs)) {
    var path: any = py.get(ir, "path");
    var semantic_ast: any = py.get(ir, "semantic_ast", {});
    var symbol: any;
    for (symbol of py.iter(normalizeSymbols(semantic_ast))) {
      py.listAppend(entities, {"id": py.get(symbol, "name"), "owner": path});
      py.listAppend(relationships, {"from": path, "to": py.get(symbol, "name"), "relation": "owns"});
    }
  }
  return {"entities": py.slice(entities, null, 10000), "relationships": py.slice(relationships, null, 10000), "bounded": true};
}
export { normalizeSymbols };
