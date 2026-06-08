/**
 * Converted from Python: core/evidence/explanatory_divergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelExplanatoryDivergence(alternatives: any): any {
  return {"divergence": py.len(alternatives), "preserved": (py.len(alternatives) > 0), "fixation_blocked": (py.len(alternatives) > 1)};
}
