/**
 * Converted from Python: core/repository/recursive/monorepo_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function detectMonorepo(text: any): any {
  var src: any = py.or2(text, () => (""));
  var workspaces: any = py.sorted(py.toSet(py.reFindall("(?:packages/[\\w\\-./]+|workspace[s]?)", src, "i")));
  return {"workspaces": workspaces};
}
