/**
 * Converted from Python: core/evidence/recursive_guardianship_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveGuardianship(centrality: any, depth: any): any {
  var guardianship: any = py.and2(centrality, () => ((depth >= 2)));
  return {"guardianship": guardianship, "suppress": guardianship, "paternalism_blocked": true};
}
