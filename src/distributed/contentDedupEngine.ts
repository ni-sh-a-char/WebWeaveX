/**
 * Converted from Python: core/distributed/content_dedup_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function dedupContents(items: any): any {
  var seen: Set<any> = new Set();
  var out: any[] = [];
  var i: any;
  for (i of py.iter(py.or2(items, () => ([])))) {
    if (!py.contains(seen, i)) {
      py.setAdd(seen, i);
      py.listAppend(out, i);
    }
  }
  return out;
}
