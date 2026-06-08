/**
 * Converted from Python: core/evidence/recursive_novelty_preservation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveRecursiveNovelty(novelty: any, depth: any): any {
  var decay_risk: any = py.and2((depth >= 5), () => ((py.get(novelty, "novelty", 0) < py.F(0.15))));
  return {"preserved": true, "decay_risk": decay_risk, "decay_suppressed": decay_risk};
}
