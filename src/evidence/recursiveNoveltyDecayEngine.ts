/**
 * Converted from Python: core/evidence/recursive_novelty_decay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resistNoveltyDecay(novelty: any, depth: any): any {
  var decay: any = py.and2((depth >= 4), () => ((novelty < py.F(0.2))));
  return {"decay_risk": decay, "resist": true, "exhaustion_blocked": decay};
}
