/**
 * Converted from Python: core/security/hardening/parser_sandbox_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function sandboxText(text: any, max_bytes: any = 5000000): any {
  var raw: any = py.encode(py.or2(text, () => ("")), "utf-8");
  return py.decode(py.slice(raw, null, max_bytes), "utf-8");
}
