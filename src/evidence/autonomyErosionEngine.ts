/**
 * Converted from Python: core/evidence/autonomy_erosion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resistAutonomyErosion(autonomy_ok: any, depth: any): any {
  var erosion: any = py.and2((depth >= 4), () => (!py.truthy(autonomy_ok)));
  return {"erosion_risk": erosion, "resist": true, "erosion_suppressed": erosion};
}
