/**
 * Converted from Python: core/runtime_language/wwx_parser.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseWwx(source: any): any {
  var statements: any[] = [];
  var index: any;
  var line: any;
  for ([index, line] of py.enumerate(py.splitlines(py.strip(source)))) {
    var stripped: any = py.strip(line);
    if ((!py.truthy(stripped) || py.truthy(py.startswith(stripped, "#")))) {
      continue;
    }
    var parts: any = py.split(stripped);
    var verb: any = String(py.at(parts, 0)).toUpperCase();
    var target: any = ((py.len(parts) > 1) ? py.at(parts, 1) : "");
    py.listAppend(statements, {"verb": verb, "target": target, "args": py.slice(parts, 2, null), "line": index});
  }
  return {"statements": statements, "bounded": true};
}
