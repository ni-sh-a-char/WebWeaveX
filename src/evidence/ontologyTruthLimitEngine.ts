/**
 * Converted from Python: core/evidence/ontology_truth_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function ontologyTruthLimits(boundaries: any): any {
  return {"self_confirmation_allowed": false, "equivalence": py.get(boundaries, "equivalence_allowed", false)};
}
