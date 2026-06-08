/**
 * Converted from Python: core/evidence/ontology_competition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelOntologyCompetition(entities: any, depth: any): any {
  return {"competitive": py.or2((py.len(entities) > 1), () => ((depth < 3))), "monopoly_suppressed": true, "dominance_allowed": false, "alternatives_required": (py.len(entities) > 0)};
}
