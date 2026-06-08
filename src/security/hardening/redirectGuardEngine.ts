/**
 * Converted from Python: core/security/hardening/redirect_guard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function redirectGuard(chain: any, max_hops: any = 10): any {
  return {"ok": (py.len(py.or2(chain, () => ([]))) <= max_hops)};
}
