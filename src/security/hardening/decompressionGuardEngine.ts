/**
 * Converted from Python: core/security/hardening/decompression_guard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function decompressionGuard(compressed: any, expanded: any, ratio_limit: any = 100): any {
  var ratio: any = py.div(expanded, py.max([1, compressed]));
  return {"ok": py.le(ratio, ratio_limit), "ratio": ratio};
}
