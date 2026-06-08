/**
 * Converted from Python: core/distributed/crawl_diff_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeCrawlDiffV2(previous: any, current: any): any {
  var p: any = py.toSet(py.or2(previous, () => ([])));
  var c: any = py.toSet(py.or2(current, () => ([])));
  return {"added": py.sorted(py.sub(c, p)), "removed": py.sorted(py.sub(p, c)), "unchanged": py.sorted(py.bitand(c, p))};
}
