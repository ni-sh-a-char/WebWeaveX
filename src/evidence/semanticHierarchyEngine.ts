/**
 * Converted from Python: core/evidence/semantic_hierarchy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectSemanticHierarchyPermanence(depth: any, hierarchy_locked: any): any {
  var permanent: any = py.and2(hierarchy_locked, () => ((depth >= 3)));
  return {"permanent": permanent, "suppress": permanent, "aristocracy_blocked": true};
}
