/**
 * Converted from Python: core/security/hardening/timeout_guard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function timeoutGuard(elapsed_ms: any, limit_ms: any = py.F(10000.0)): any {
  return {"ok": py.le(elapsed_ms, limit_ms)};
}
