/**
 * Converted from Python: core/security/payload_limits.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_HTML_SIZE: any = 2000000;
export let MAX_MARKDOWN_SIZE: any = 2000000;
export let MAX_JSON_SIZE: any = 2000000;
export let MAX_GRAPH_SIZE: any = 500;
export function enforceTextLimit(text: any, limit: any): any {
  var safe: any = py.or2(text, () => (""));
  if ((py.len(py.encode(safe, "utf-8")) > limit)) {
    return py.decode(py.slice(py.encode(safe, "utf-8"), null, limit), "utf-8");
  }
  return safe;
}
