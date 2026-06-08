/**
 * Converted from Python: core/security/path_traversal_guard.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function safePath(path: any): any {
  var p: any = py.replace(py.or2(path, () => ("")), "\\", "/");
  return py.and2(!py.contains(p, "../"), () => (!py.truthy(py.startswith(p, "/"))));
}
