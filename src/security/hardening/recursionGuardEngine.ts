/**
 * Converted from Python: core/security/hardening/recursion_guard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function recursionGuard(depth: any, limit: any = 6): any {
  return {"ok": py.le(depth, limit)};
}
