/**
 * Converted from Python: core/evidence/ontology_self_determination_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelOntologySelfDetermination(entity_count: any): any {
  return {"self_determined": !py.eq(entity_count, 1), "submission_blocked": true, "reliance_blocked": true};
}
