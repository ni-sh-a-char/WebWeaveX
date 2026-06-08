/**
 * Converted from Python: core/repository/reconstruction/ownership_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function inferOwnershipDomains(paths: any): any {
  var domains: Record<string, any> = {};
  var p: any;
  for (p of py.iter(py.sorted(py.toSet(py.or2(paths, () => ([])))))) {
    var key: any = (py.contains(p, "/") ? py.at(py.split(p, "/"), 0) : "root");
    py.listAppend(py.setdefault(domains, key, []), p);
  }
  return {"domains": py.iter(py.sorted(py.items(domains))).map(([k, v]: any) => ({"name": k, "paths": py.sorted(v)}))};
}
