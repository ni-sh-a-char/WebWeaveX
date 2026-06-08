/**
 * Converted from Python: core/crawling/advanced/robots_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function parseRobots(text: any): any {
  var allow: any[] = [];
  var deny: any[] = [];
  var ln: any;
  for (ln of py.iter(py.splitlines(py.or2(text, () => (""))))) {
    var x: any = py.strip(ln);
    var lx: any = String(x).toLowerCase();
    if (py.truthy(py.startswith(lx, "allow:"))) {
      py.listAppend(allow, py.strip(py.at(py.split(x, ":", 1), 1)));
    }
    if (py.truthy(py.startswith(lx, "disallow:"))) {
      py.listAppend(deny, py.strip(py.at(py.split(x, ":", 1), 1)));
    }
  }
  return {"allow": py.sorted(py.toSet(allow)), "deny": py.sorted(py.toSet(deny))};
}
