/**
 * Converted from Python: core/evidence/cognitive_gravity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectCognitiveGravityWell(high_confidence: any, low_diversity: any, depth: any): any {
  var gravity: any = py.and2(high_confidence, () => (py.and2(low_diversity, () => ((depth >= 2)))));
  return {"gravity_well": gravity, "suppress": gravity, "sink_state_blocked": gravity};
}
