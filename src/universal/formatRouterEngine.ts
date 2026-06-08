/**
 * Converted from Python: core/universal/format_router_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function routeFormat(content_type: any, source_url: any = ""): any {
  var c: any = String(py.or2(content_type, () => (""))).toLowerCase();
  var u: any = String(py.or2(source_url, () => (""))).toLowerCase();
  if ((py.contains(c, "json") || py.truthy(py.endswith(u, ".json")))) {
    return "json";
  }
  if ((py.contains(c, "yaml") || py.truthy(py.endswith(u, [".yaml", ".yml"])))) {
    return "yaml";
  }
  if ((py.contains(c, "xml") || py.truthy(py.endswith(u, ".xml")))) {
    return "xml";
  }
  if ((py.contains(c, "markdown") || py.truthy(py.endswith(u, ".md")))) {
    return "markdown";
  }
  if ((py.contains(c, "pdf") || py.truthy(py.endswith(u, ".pdf")))) {
    return "pdf";
  }
  if ((py.contains(c, "html") || py.truthy(py.startswith(u, "http")))) {
    return "html";
  }
  return "text";
}
