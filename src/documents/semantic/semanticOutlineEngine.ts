/**
 * Converted from Python: core/documents/semantic/semantic_outline_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticOutline(text: any): any {
  var source: any = py.or2(text, () => (""));
  var headings: any[] = [];
  var m: any;
  for (m of py.iter(py.reFinditer("^(#+)\\s+(.+)$", source, "m"))) {
    py.listAppend(headings, {"level": py.len(m.group(1)), "title": py.strip(m.group(2))});
  }
  return {"headings": headings, "count": py.len(headings)};
}
