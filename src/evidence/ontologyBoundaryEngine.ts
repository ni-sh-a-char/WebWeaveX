/**
 * Converted from Python: core/evidence/ontology_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelOntologyBoundaries(evidence: any, inferred: any = false): any {
  var allowed: any = py.and2((py.len(evidence) >= 2), () => (!py.truthy(inferred)));
  return {"expansion_allowed": allowed, "inheritance_allowed": allowed, "equivalence_allowed": allowed, "merge_allowed": (py.len(evidence) >= 3)};
}
