/**
 * Converted from Python: core/security/resource_budget.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let DEFAULT_BYTE_LIMIT: any = 50000000;
export function enforceResourceBudget(bytes_used: any, limit: any = DEFAULT_BYTE_LIMIT): any {
  var used: any = py.max([0, py.toInt(bytes_used)]);
  var lim: any = py.max([1, py.toInt(limit)]);
  var ok: any = py.le(used, lim);
  return {"ok": ok, "allowed": ok, "bytes_used": used, "limit": lim};
}
