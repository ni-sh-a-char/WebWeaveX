/**
 * Converted from Python: core/evidence/recursive_capture_resistance_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelCaptureResistance(suppressed: any): any {
  return {"resistant": true, "capture_events_suppressed": py.len(suppressed), "domination_blocked": py.truthy(suppressed)};
}
