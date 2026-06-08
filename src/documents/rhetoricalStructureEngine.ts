/**
 * Converted from Python: core/documents/rhetorical_structure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractRhetoricalStructure(text: any): any {
  var m;
  var lines: any = py.splitlines(py.or2(text, () => ("")));
  var units: any[] = [];
  var i: any;
  var ln: any;
  for ([i, ln] of py.enumerate(lines)) {
    if (py.truthy((m = py.reMatch("^(#{1,6})\\s+(.+)$", py.strip(ln), "")))) {
      py.listAppend(units, {"type": "heading", "level": py.len(m.group(1)), "title": m.group(2), "line": i});
    } else if (py.truthy(py.reMatch("^[-*]\\s+", py.strip(ln), ""))) {
      py.listAppend(units, {"type": "list_item", "line": i});
    } else if (py.truthy(py.startswith(py.strip(ln), "```"))) {
      py.listAppend(units, {"type": "code_fence", "line": i});
    }
  }
  return {"units": units, "unit_count": py.len(units), "deterministic_inputs": [`units=${py.toStr(py.len(units))}`]};
}
