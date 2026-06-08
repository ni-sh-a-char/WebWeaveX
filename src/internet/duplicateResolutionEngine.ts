/**
 * Converted from Python: core/internet/duplicate_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveDuplicates(items: any): any {
  var seen: Set<any> = new Set();
  var out: any[] = [];
  var item: any;
  for (item of py.iter(py.sorted(py.or2(items, () => ([])), {key: ((x: any) => py.toStr(x)) as (item: any) => any}))) {
    var key: any = py.toStr(item);
    if (py.contains(seen, key)) {
      continue;
    }
    py.setAdd(seen, key);
    py.listAppend(out, item);
  }
  return out;
}
