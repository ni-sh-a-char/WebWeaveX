/**
 * Converted from Python: core/semantic/ambiguity_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { preserveAmbiguities } from "./ambiguityPreservationEngine.js";

export function reasonAmbiguity(candidates: any, evidence: any): any {
  var preserved: any = preserveAmbiguities(candidates, evidence);
  return {"ambiguities": py.get(preserved, "ambiguities", []), "preserved": py.get(preserved, "preserved", false), "evidence": py.get(preserved, "evidence", []), "lineage": py.get(preserved, "lineage", {}), "competing_interpretations": py.get(preserved, "ambiguities", [])};
}
export { preserveAmbiguities };
