/**
 * Converted from Python: core/knowledge/semantic_merge_validator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { mergeWithEvidence } from "./semanticMergeRigorEngine.js";
import { detectOntologyConflicts } from "./ontologyConflictEngine.js";

export function validateSemanticMerge(sources: any, edges: any): any {
  var merge: any = mergeWithEvidence(sources);
  var conflicts: any = detectOntologyConflicts(edges);
  var allowed: any = py.and2(py.get(merge, "merged", false), () => ((py.get(conflicts, "pressure", 0) < py.F(0.75))));
  return {"allowed": allowed, "merge": merge, "conflicts": conflicts, "rejected_reason": (py.truthy(allowed) ? null : "merge_or_conflict_blocked")};
}
export { detectOntologyConflicts, mergeWithEvidence };
