/**
 * Converted from Python: core/memory/semantic_reconciliation_memory.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconcileOntologyEdges } from "../knowledge/ontologyReconciliationEngine.js";

export function reconcileMemoryStates(states: any): any {
  var edges: any[] = [];
  var s: any;
  for (s of py.iter(states)) {
    py.extend(edges, py.or2(py.get(s, "relations", py.get(s, "edges", [])), () => ([])));
  }
  var recon: any = reconcileOntologyEdges(((Array.isArray(edges)) ? edges : []));
  return {"states": py.len(states), "reconciliation": recon, "deterministic": true};
}
export { reconcileOntologyEdges };
