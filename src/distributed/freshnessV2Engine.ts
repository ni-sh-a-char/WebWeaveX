/**
 * Converted from Python: core/distributed/freshness_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeFreshnessV2(previous_content_hashes: any, current_content_hashes: any): any {
  var prev: any = py.or2(previous_content_hashes, () => ({}));
  var curr: any = py.or2(current_content_hashes, () => ({}));
  var changed: any = py.sorted(py.iter(py.sorted(curr)).filter((u: any) => !py.eq(py.get(prev, u), py.get(curr, u))).map((u: any) => u));
  var unchanged: any = py.sorted(py.iter(py.sorted(curr)).filter((u: any) => py.eq(py.get(prev, u), py.get(curr, u))).map((u: any) => u));
  return {"changed": changed, "unchanged": unchanged};
}
