/**
 * Converted from Python: core/evidence/explanatory_fixation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectExplanatoryFixation(alternative_count: any, depth: any): any {
  var fixation: any = py.and2((alternative_count <= 1), () => ((depth >= 2)));
  return {"fixation": fixation, "suppress": fixation};
}
