/**
 * Converted from Python: core/repository/ownership_inference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function inferOwnership(paths: any): any {
  var owners: Record<string, any> = {};
  var p: any;
  for (p of py.iter(py.sorted(py.toSet(py.or2(paths, () => ([])))))) {
    var key: any = (py.contains(p, "/") ? py.at(py.split(p, "/"), 0) : "root");
    py.listAppend(py.setdefault(owners, key, []), p);
  }
  return {"ownership": py.iter(py.sorted(py.items(owners))).map(([k, v]: any) => ({"team": k, "paths": py.sorted(v)}))};
}
