/**
 * Converted from Python: core/internet/intelligence/duplicate_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function resolveDuplicateSources(items: any): any {
  var seen: Set<any> = new Set();
  var out: any[] = [];
  var i: any;
  for (i of py.iter(py.sorted(py.or2(items, () => ([])), {key: ((x: any) => py.toStr(x)) as (item: any) => any}))) {
    var k: any = py.toStr(i);
    if (py.contains(seen, k)) {
      continue;
    }
    py.setAdd(seen, k);
    py.listAppend(out, i);
  }
  return out;
}
