/**
 * Converted from Python: core/security/xml_guard.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function safeXmlSize(size: any, limit: any = 5000000): any {
  return py.le(size, limit);
}
