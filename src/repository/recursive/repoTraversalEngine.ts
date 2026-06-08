/**
 * Converted from Python: core/repository/recursive/repo_traversal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function traverseRepo(text: any): any {
  var paths: any = py.sorted(py.toSet(py.reFindall("[A-Za-z0-9_./-]+", py.or2(text, () => ("")), "")));
  return {"paths": py.slice(paths, null, 5000)};
}
