/**
 * Converted from Python: core/documents/heading_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractHeadings(text: any): any {
  var src: any = py.or2(text, () => (""));
  var md: any = py.iter(py.reFindall("^(#{1,6})\\s+(.+)$", src, "m")).map(([h, t]: any) => ({"level": py.len(h), "title": py.strip(t)}));
  var html: any = py.iter(py.reFindall("<h([1-6])[^>]*>(.*?)</h\\1>", src, "is")).map(([n, t]: any) => ({"level": py.toInt(n), "title": py.strip(t)}));
  var headings: any = py.sorted(py.add(md, html), {key: ((x: any) => [py.at(x, "level"), py.at(x, "title")]) as (item: any) => any});
  return {"headings": headings};
}
