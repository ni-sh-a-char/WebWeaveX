/**
 * Converted from Python: core/security/hardening/ssrf_guard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function ssrfGuard(url: any): any {
  var p: any = py.urlparse(py.or2(url, () => ("")));
  if (!py.contains(new Set(["http", "https"]), String(p.scheme).toLowerCase())) {
    return {"ok": false};
  }
  var host: any = String(py.or2(p.hostname, () => (""))).toLowerCase();
  if (py.contains(new Set(["localhost", "127.0.0.1", "::1"]), host)) {
    return {"ok": false};
  }
  try {
    var ip: any = py.ipAddress(host);
    if ((py.truthy(ip.is_private) || py.truthy(ip.is_loopback))) {
      return {"ok": false};
    }
  } catch (_e: any) {
  }
  return {"ok": true};
}
