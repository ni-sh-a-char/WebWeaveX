/**
 * Converted from Python: core/evidence/ontology_freedom_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveOntologyFreedom(competition: any): any {
  return {"free": py.get(competition, "competitive", true), "caste_blocked": true};
}
