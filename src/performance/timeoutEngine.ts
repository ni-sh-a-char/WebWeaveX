/**
 * Converted from Python: core/performance/timeout_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function withinTimeout(elapsed_ms: any, limit_ms: any = py.F(10000.0)): any {
  return py.le(elapsed_ms, limit_ms);
}
