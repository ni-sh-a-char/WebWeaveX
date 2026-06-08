/**
 * Converted from Python: core/crawling/link_classifier.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function classifyLink(url: any): any {
  var u: any = String(py.or2(url, () => (""))).toLowerCase();
  if (py.contains(u, "github.com")) {
    return "repository";
  }
  if ((py.contains(u, "docs") || py.contains(u, "readthedocs"))) {
    return "documentation";
  }
  if ((py.truthy(py.startswith(u, "http://")) || py.truthy(py.startswith(u, "https://")))) {
    return "web";
  }
  return "unknown";
}
