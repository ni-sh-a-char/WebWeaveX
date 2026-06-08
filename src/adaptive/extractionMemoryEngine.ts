/**
 * Converted from Python: core/adaptive/extraction_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";

export function rememberExtractionRuntime(memory: any, update: any): any {
  var merged: any = py.pyDict(memory);
  py.setdefault(merged, "selectors", {});
  py.setdefault(merged, "healed_selectors", {});
  py.setdefault(merged, "pagination_patterns", []);
  py.setdefault(merged, "modal_solutions", []);
  py.setdefault(merged, "interaction_chains", []);
  var key: any;
  var value: any;
  for ([key, value] of py.items(update)) {
    py.setItem(merged, key, value);
  }
  py.setItem(merged, "bounded", true);
  return merged;
}
export function restoreExtractionRuntime(memory: any): any {
  return {"memory": memory, "restored": py.truthy(memory), "bounded": true};
}
export function saveAdaptiveMemory(path: any, memory: any, key: any): any {
  var encrypted: any = encryptSessionState(memory, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(encrypted, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadAdaptiveMemory(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "memory": _emptyMemory(), "bounded": true};
  }
  var encrypted: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptSessionState(encrypted, key);
  return {"available": true, "memory": py.get(decrypted, "session", _emptyMemory()), "algorithm": "kaalka", "bounded": true};
}
export function _emptyMemory(): any {
  return {"selectors": {}, "healed_selectors": {}, "pagination_patterns": [], "modal_solutions": [], "interaction_chains": [], "bounded": true};
}
export { decryptSessionState, encryptSessionState };
