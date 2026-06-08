/**
 * Converted from Python: core/native/native_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";

export function saveNativeRuntime(path: any, runtime: any, key: any): any {
  var encrypted: any = encryptSessionState(runtime, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(encrypted, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadNativeRuntime(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "runtime": _emptyRuntime(), "bounded": true};
  }
  var encrypted: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptSessionState(encrypted, key);
  return {"available": true, "runtime": py.get(decrypted, "session", _emptyRuntime()), "algorithm": "kaalka", "bounded": true};
}
export function rememberNativeRuntime(memory: any, update: any): any {
  var merged: any = py.pyDict(memory);
  var key: any;
  for (key of py.iter(["accessibility_trees", "windows", "workflows", "runtime_graphs", "electron_state", "terminal_streams"])) {
    py.setdefault(merged, key, py.get(update, key, py.get(merged, key, {})));
  }
  py.update(merged, update);
  py.setItem(merged, "bounded", true);
  return merged;
}
export function _emptyRuntime(): any {
  return {"accessibility_trees": {}, "windows": {}, "workflows": {}, "runtime_graphs": {}, "electron_state": {}, "terminal_streams": {}, "bounded": true};
}
export { decryptSessionState, encryptSessionState };
