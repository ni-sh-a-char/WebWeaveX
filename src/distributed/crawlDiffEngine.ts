/**
 * Converted from Python: core/distributed/crawl_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function crawlDiff(a: any, b: any): any {
  var sa: any = py.toSet(py.or2(a, () => ([])));
  var sb: any = py.toSet(py.or2(b, () => ([])));
  return {"added": py.sorted(py.sub(sb, sa)), "removed": py.sorted(py.sub(sa, sb))};
}
