/**
 * Converted from Python: core/knowledge/ontology_conflict_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import { detectOntologyConflicts } from "./ontologyConflictEngine.js";

export function runtimeOntologyConflicts(edges: any): any {
  return detectOntologyConflicts(edges);
}
export { detectOntologyConflicts };
