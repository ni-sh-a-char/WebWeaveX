/**
 * Converted from Python: core/internet/freshness_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeFreshness(version_map: any): any {
  var ordered: any = py.sorted(py.items(py.or2(version_map, () => ({}))));
  return {"ordered_versions": ordered, "count": py.len(ordered)};
}
