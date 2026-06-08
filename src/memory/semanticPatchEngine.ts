/**
 * Converted from Python: core/memory/semantic_patch_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSemanticPatch(old: any, new_: any): any {
  var added: Record<string, any> = {};
  var removed: Record<string, any> = {};
  var key: any;
  for (key of py.iter(new_)) {
    if (!py.contains(old, key)) {
      py.setItem(added, key, py.at(new_, key));
    }
  }
  for (key of py.iter(old)) {
    if (!py.contains(new_, key)) {
      py.setItem(removed, key, py.at(old, key));
    }
  }
  return {"added": added, "removed": removed};
}
