/**
 * Converted from Python: core/internet/intelligence/semantic_source_merge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function mergeSemanticSources(records: any): any {
  var merged: Record<string, any> = {};
  var r: any;
  for (r of py.iter(py.or2(records, () => ([])))) {
    var k: any;
    var v: any;
    for ([k, v] of py.iter(py.sorted(py.items(py.or2(r, () => ({})))))) {
      py.setAdd(py.setdefault(merged, k, new Set()), py.toStr(v));
    }
  }
  return Object.fromEntries(py.iter(py.sorted(py.items(merged))).map(([k, v]: any) => ([k, py.sorted(v)] as [any, any])));
}
