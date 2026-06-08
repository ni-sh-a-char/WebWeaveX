/**
 * Converted from Python: core/database/persistent_semantic_store_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function persistSemanticState(path: any, state: any): any {
  var target: any = py.path(path);
  target.write_text(py.jsonDumps(state, {sortKeys: true, indent: 2, defaultStr: true}), "utf-8");
  return {"persisted": true, "path": py.toStr(target)};
}
