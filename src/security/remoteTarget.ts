/**
 * Converted from Python: core/security/remote_target.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function isSafeRemoteTarget(url: any): any {
  var parsed: any = py.urlparse(py.or2(url, () => ("")));
  if (!py.contains(new Set(["http", "https"]), String(parsed.scheme).toLowerCase())) {
    return false;
  }
  var host: any = String(py.or2(parsed.hostname, () => (""))).toLowerCase();
  if (py.contains(new Set(["localhost", "127.0.0.1", "::1"]), host)) {
    return false;
  }
  try {
    var ip: any = py.ipAddress(host);
    if ((py.truthy(ip.is_private) || py.truthy(ip.is_loopback) || py.truthy(ip.is_link_local))) {
      return false;
    }
  } catch (_e: any) {
  }
  return true;
}
