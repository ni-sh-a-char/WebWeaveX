/**
 * Converted from Python: core/performance/memory_budget_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function memoryBudget(bytes_used: any, limit: any = 1000000000): any {
  var used: any = py.max([0, py.toInt(bytes_used)]);
  var lim: any = py.max([1, py.toInt(limit)]);
  return {"ok": py.le(used, lim), "bytes_used": used, "limit": lim};
}
