/**
 * Converted from Python: core/security/url_validator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ALLOWED_SCHEMES: any = new Set(["http", "https"]);
export let BLOCKED_SCHEMES: any = new Set(["file", "smb", "ftp"]);
export function isSafeUrl(url: any): any {
  try {
    var p: any = py.urlparse(url);
    if (py.contains(BLOCKED_SCHEMES, p.scheme)) {
      return false;
    }
    if ((!py.contains(ALLOWED_SCHEMES, p.scheme) || !py.truthy(p.hostname))) {
      return false;
    }
    var host: any = String(p.hostname).toLowerCase();
    if (py.contains(new Set(["localhost", "127.0.0.1"]), host)) {
      return false;
    }
    try {
      var ip: any = py.ipAddress(host);
      if ((py.truthy(ip.is_private) || py.truthy(ip.is_loopback) || py.truthy(ip.is_link_local) || py.truthy(ip.is_reserved) || py.truthy(ip.is_multicast))) {
        return false;
      }
    } catch (_e: any) {
    }
    return true;
  } catch (_e: any) {
    return false;
  }
}
