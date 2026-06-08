/**
 * Converted from Python: core/knowledge/knowledge_reconciliation_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import { reconcileOntologyEdges } from "./ontologyReconciliationEngine.js";
import { validateSemanticMerge } from "./semanticMergeValidator.js";

export function reconcileKnowledgeRuntime(sources: any, edges: any): any {
  var merge: any = validateSemanticMerge(sources, edges);
  var recon: any = reconcileOntologyEdges(edges);
  return {"merge": merge, "reconciliation": recon, "deterministic": true};
}
export { reconcileOntologyEdges, validateSemanticMerge };
