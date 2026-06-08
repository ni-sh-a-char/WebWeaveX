/**
 * Converted from Python: core/evidence/ontology_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function ontologyLimits(boundaries: any): any {
  return {"inheritance": py.get(boundaries, "inheritance_allowed", false), "equivalence": py.get(boundaries, "equivalence_allowed", false)};
}
