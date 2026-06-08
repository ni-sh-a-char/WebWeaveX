/**
 * Converted from Python: core/repository/reconstruction/topology_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function reconstructTopology(paths: any): any {
  var modules: any = py.sorted(py.toSet(py.or2(paths, () => ([]))));
  var services: any = py.sorted(py.toSet(py.iter(modules).filter((p: any) => py.contains(p, "/")).map((p: any) => py.at(py.split(p, "/"), 0))));
  var layers: any = py.sorted(py.toSet(py.iter(modules).filter((p: any) => (py.count(p, "/") >= 2)).map((p: any) => py.at(py.split(p, "/"), 1))));
  var boundaries: any = py.sorted(py.toSet(py.iter(modules).filter((p: any) => py.contains(p, "/")).map((p: any) => py.at(py.rsplit(p, "/", 1), 0))));
  return {"modules": modules, "services": services, "layers": layers, "boundaries": boundaries};
}
