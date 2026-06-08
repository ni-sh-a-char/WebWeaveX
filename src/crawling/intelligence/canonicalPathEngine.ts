/**
 * Converted from Python: core/crawling/intelligence/canonical_path_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function canonicalPaths(urls: any): any {
  var out: any[] = [];
  var u: any;
  for (u of py.iter(py.sorted(py.toSet(py.or2(urls, () => ([])))))) {
    var p: any = py.urlparse(u);
    py.listAppend(out, py.urlunparse([String(p.scheme).toLowerCase(), String(p.netloc).toLowerCase(), py.or2(p.path, () => ("/")), "", "", ""]));
  }
  return py.sorted(py.toSet(out));
}
