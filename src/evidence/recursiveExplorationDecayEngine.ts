/**
 * Converted from Python: core/evidence/recursive_exploration_decay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resistExplorationDecay(exploratory: any, depth: any): any {
  var decay: any = py.and2((depth >= 5), () => (!py.truthy(exploratory)));
  return {"decay_risk": decay, "resist": true};
}
