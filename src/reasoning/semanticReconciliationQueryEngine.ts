/**
 * Converted from Python: core/reasoning/semantic_reconciliation_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { reconcileOntologyEdges } from "../knowledge/ontologyReconciliationEngine.js";

export function reconcileQuery(entities: any, edges: any): any {
  var recon: any = reconcileOntologyEdges(edges);
  return {"entities": entities, "reconciliation": recon, "explainable": true};
}
export { reconcileOntologyEdges };
