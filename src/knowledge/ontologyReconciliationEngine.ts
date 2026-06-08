/**
 * Converted from Python: core/knowledge/ontology_reconciliation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { mergeWithEvidence } from "./semanticMergeRigorEngine.js";
import { stampOntologyLineage } from "./ontologyLineageEngine.js";

export function reconcileOntologyEdges(edges: any): any {
  var reconciled: any[] = [];
  var rejected: any[] = [];
  var e: any;
  for (e of py.iter(py.or2(edges, () => ([])))) {
    var ev: any = py.or2(py.get(e, "evidence", []), () => ([]));
    if (!py.truthy(ev)) {
      py.listAppend(rejected, {"edge": e, "reason": "missing_evidence"});
      continue;
    }
    var stamped: any = stampOntologyLineage(e, "reconcile");
    py.listAppend(reconciled, stamped);
  }
  var merge: any = mergeWithEvidence(py.iter(reconciled).map((e: any) => ({"evidence": py.get(e, "evidence", [])})));
  return {"reconciled": reconciled, "rejected": rejected, "merge": merge, "lineage": {"stage": "ontology_reconciliation", "count": py.len(reconciled)}};
}
export { mergeWithEvidence, stampOntologyLineage };
