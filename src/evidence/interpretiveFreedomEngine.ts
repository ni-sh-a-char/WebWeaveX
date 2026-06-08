/**
 * Converted from Python: core/evidence/interpretive_freedom_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveInterpretiveFreedom(autonomy: any): any {
  return {"free": py.get(autonomy, "autonomous", true), "empire_blocked": true};
}
