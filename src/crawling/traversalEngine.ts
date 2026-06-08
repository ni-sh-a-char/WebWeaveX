/**
 * Converted from Python: core/crawling/traversal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function discoverLinks(base_url: any, text: any): any {
  var src: any = py.or2(text, () => (""));
  var hrefs: any = py.reFindall("href=[\"']([^\"']+)[\"']", src, "i");
  var md: any = py.reFindall("\\[[^\\]]+\\]\\(([^)]+)\\)", src, "");
  var out: any[] = [];
  var u: any;
  for (u of py.iter(py.add(hrefs, md))) {
    var full: any = py.urljoin(base_url, u);
    if ((py.truthy(py.startswith(full, "http://")) || py.truthy(py.startswith(full, "https://")))) {
      py.listAppend(out, full);
    }
  }
  return py.sorted(py.toSet(out));
}
