/**
 * Converted from Python: core/query/semantic_query_planner.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function planSemanticQuery(intent: any, targets: any): any {
  var steps: any[] = [];
  if (py.contains(intent, "graph")) {
    py.listAppend(steps, "traverse_graph");
  }
  if (py.contains(intent, "document")) {
    py.listAppend(steps, "query_documents");
  }
  if (py.contains(intent, "repository")) {
    py.listAppend(steps, "query_repository");
  }
  if (!py.truthy(steps)) {
    steps = ["query_semantics"];
  }
  return {"intent": intent, "steps": steps, "targets": py.sorted(targets), "deterministic": true};
}
