/**
 * Converted from Python: core/security/hardening/memory_guard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function memoryGuard(bytes_used: any, limit: any = 1000000000): any {
  return {"ok": py.le(bytes_used, limit)};
}
