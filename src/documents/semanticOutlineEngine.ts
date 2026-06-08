/**
 * Converted from Python: core/documents/semantic_outline_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractSemanticOutline(text: any): any {
  var headings: any[] = [];
  var line: any;
  for (line of py.iter(py.splitlines(py.or2(text, () => (""))))) {
    var match: any = py.reMatch("^(#{1,6})\\s+(.+)$", py.strip(line), "");
    if (py.truthy(match)) {
      py.listAppend(headings, {"level": py.toStr(py.len(match.group(1))), "title": py.strip(match.group(2))});
    }
  }
  return {"headings": headings, "heading_count": py.len(headings)};
}
