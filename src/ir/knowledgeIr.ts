/**
 * Converted from Python: core/ir/knowledge_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { emptyConfidence, emptyLineage, mergeEvidence } from "./_base.js";
import { reconcileOntologyEdges } from "../knowledge/ontologyReconciliationEngine.js";
import { resolveSemanticIdentities } from "../knowledge/semanticIdentityResolver.js";
import { detectOntologyConflicts } from "../knowledge/ontologyConflictEngine.js";

export let KnowledgeIR: any = py.at(Object, [py.toStr, Object]);
export function emptyKnowledgeIr(): any {
  return {"entities": [], "relations": [], "ontology": [], "semantic_identity": [], "contradictions": [], "evidence": [], "lineage": [], "reconciliation": {}, "confidence": emptyConfidence()};
}
export function compileKnowledgeIr(entities: any, edges: any): any {
  var recon: any = reconcileOntologyEdges(edges);
  var ids: any = resolveSemanticIdentities(entities);
  var conflicts: any = detectOntologyConflicts(edges);
  var ir: any = emptyKnowledgeIr();
  py.setItem(ir, "entities", entities);
  py.setItem(ir, "relations", py.get(recon, "reconciled", []));
  py.setItem(ir, "ontology", edges);
  py.setItem(ir, "semantic_identity", py.get(ids, "entities", []));
  py.setItem(ir, "contradictions", py.get(conflicts, "conflicts", []));
  py.setItem(ir, "evidence", py.iter(edges).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => py.get(e, "evidence", [])));
  py.setItem(ir, "lineage", [py.get(recon, "lineage", {})]);
  py.setItem(ir, "reconciliation", recon);
  py.setItem(ir, "confidence", {"score": (!py.truthy(py.get(conflicts, "conflicts")) ? py.F(0.9) : py.F(0.5)), "basis": [], "deterministic": true});
  return ir;
}
export { detectOntologyConflicts, emptyConfidence, emptyLineage, mergeEvidence, reconcileOntologyEdges, resolveSemanticIdentities };
