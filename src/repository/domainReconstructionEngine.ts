/**
 * Converted from Python: core/repository/domain_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructDomainModel(modules: any): any {
  var domains: Record<string, any> = {};
  var m: any;
  for (m of py.iter(py.sorted(py.toSet(py.or2(modules, () => ([])))))) {
    var key: any = (py.contains(m, "/") ? py.at(py.split(m, "/"), 0) : m);
    py.listAppend(py.setdefault(domains, key, []), m);
  }
  return {"domains": py.iter(py.sorted(py.items(domains))).map(([k, v]: any) => ({"name": k, "modules": py.sorted(v)}))};
}
