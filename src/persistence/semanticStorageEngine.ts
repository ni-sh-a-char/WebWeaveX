/**
 * Converted from Python: core/persistence/semantic_storage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function writeSemanticStorage(path: any, payload: any): any {
  var p: any = py.path(path);
  var encoded: any = py.jsonDumps(payload, {sortKeys: true, indent: 2, defaultStr: true});
  p.write_text(encoded, "utf-8");
  return {"path": py.toStr(p), "written": true, "bytes": py.len(encoded)};
}
