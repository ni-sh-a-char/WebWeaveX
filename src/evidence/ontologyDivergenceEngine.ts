/**
 * Converted from Python: core/evidence/ontology_divergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelOntologyDivergence(entities: any, depth: any): any {
  return {"divergence": py.len(py.toSet(entities)), "preserved": py.or2((py.len(entities) > 1), () => ((depth < 3))), "hardening_blocked": true};
}
