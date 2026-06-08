/**
 * Converted from Python: core/crawling/dedup_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function canonicalUrl(url: any): any {
  var s: any = py.urlsplit(py.strip(py.or2(url, () => (""))));
  return py.urlunsplit([String(s.scheme).toLowerCase(), String(s.netloc).toLowerCase(), py.or2(s.path, () => ("/")), s.query, ""]);
}
