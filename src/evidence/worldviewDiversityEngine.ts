/**
 * Converted from Python: core/evidence/worldview_diversity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelWorldviewDiversity(interpretations: any, contradicted: any): any {
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  return {"diverse": py.or2((py.len(interpretations) > 1), () => (py.truthy(pairs))), "convergence_suppressed": true, "worldview_lock_in": false, "alternative_worldviews": py.len(interpretations)};
}
