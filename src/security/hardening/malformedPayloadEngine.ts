/**
 * Converted from Python: core/security/hardening/malformed_payload_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function malformedPayloadGuard(text: any): any {
  var src: any = String(py.or2(text, () => (""))).toLowerCase();
  var blocked: any = py.or2(py.contains(src, "<!entity"), () => (py.contains(src, "<!doctype")));
  return {"ok": !py.truthy(blocked)};
}
