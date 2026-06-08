/**
 * Converted from Python: core/ir/ontology_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileKnowledgeIr } from "./knowledgeIr.js";

export let OntologyIR: any = py.at(Object, [py.toStr, Object]);
export function compileOntologyIr(entities: any, edges: any): any {
  var k: any = compileKnowledgeIr(entities, edges);
  return {"ontology": py.get(k, "ontology", []), "entities": py.get(k, "entities", []), "reconciliation": py.get(k, "reconciliation", {}), "confidence": py.get(k, "confidence", {})};
}
export { compileKnowledgeIr };
