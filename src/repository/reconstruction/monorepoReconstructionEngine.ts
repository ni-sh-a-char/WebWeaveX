/**
 * Converted from Python: core/repository/reconstruction/monorepo_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function reconstructMonorepo(paths: any): any {
  var p: any = py.sorted(py.toSet(py.or2(paths, () => ([]))));
  var workspaces: any = py.iter(p).filter((x: any) => (py.contains(x, "/packages/") || py.truthy(py.startswith(x, "packages/")) || py.contains(x, "/apps/"))).map((x: any) => x);
  var groups: any = py.sorted(py.toSet(py.iter(workspaces).filter((w: any) => py.contains(w, "/")).map((w: any) => py.at(py.split(w, "/"), 0))));
  return {"workspaces": workspaces, "groups": groups};
}
