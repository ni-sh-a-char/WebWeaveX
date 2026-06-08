/**
 * Converted from Python: core/internet/merge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function mergeSources(sources: any, key: any = "url"): any {
  var merged: Record<string, any> = {};
  var item: any;
  for (item of py.iter(py.or2(sources, () => ([])))) {
    if (!((item !== null && typeof item === "object" && !Array.isArray(item) && !(item instanceof Set) && !(item instanceof Map)))) {
      continue;
    }
    var k: any = py.toStr(py.get(item, key, ""));
    if (!py.truthy(k)) {
      continue;
    }
    if (!py.contains(merged, k)) {
      py.setItem(merged, k, py.pyDict(item));
      continue;
    }
    var field: any;
    var value: any;
    for ([field, value] of py.items(item)) {
      if (!py.contains(py.at(merged, k), field)) {
        py.setItem(py.at(merged, k), field, value);
      }
    }
  }
  return py.iter(py.sorted(merged)).map((k: any) => py.at(merged, k));
}
