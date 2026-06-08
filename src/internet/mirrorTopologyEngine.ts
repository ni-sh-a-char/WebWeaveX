/**
 * Converted from Python: core/internet/mirror_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectMirrorTopology(urls: any): any {
  var mirrors: any[] = [];
  var seen: Record<string, any> = {};
  var u: any;
  for (u of py.iter(py.or2(urls, () => ([])))) {
    var key: any = (py.contains(u, "//") ? py.at(py.split(py.at(py.split(u, "//"), (-1)), "/"), 0) : u);
    if (py.contains(seen, key)) {
      py.listAppend(mirrors, {"original": py.at(seen, key), "mirror": u});
    } else {
      py.setItem(seen, key, u);
    }
  }
  return {"mirrors": mirrors, "count": py.len(mirrors)};
}
