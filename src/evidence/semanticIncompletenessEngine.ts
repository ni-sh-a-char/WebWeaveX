/**
 * Converted from Python: core/evidence/semantic_incompleteness_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelIncompleteness(known: any, unknown: any, unsupported: any): any {
  return {"known": known, "unknown": py.sorted(py.toSet(py.or2(unknown, () => ([])))), "unsupported": py.sorted(py.toSet(py.or2(unsupported, () => ([])))), "incomplete": py.truthy(py.or2(unknown, () => (unsupported))), "preserved": true};
}
