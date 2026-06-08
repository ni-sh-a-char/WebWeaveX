/**
 * Converted from Python: core/application/application_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";

export function rememberApplicationRuntime(memory: any, update: any): any {
  var merged: any = py.pyDict(memory);
  var key: any;
  for (key of py.iter(["workflows", "forms", "action_graphs", "navigation_flows", "dashboard_structures"])) {
    py.setdefault(merged, key, py.get(update, key, py.get(merged, key, {})));
  }
  py.update(merged, update);
  py.setItem(merged, "bounded", true);
  return merged;
}
export function restoreApplicationRuntime(memory: any): any {
  return {"memory": memory, "restored": py.truthy(memory), "bounded": true};
}
export function saveApplicationMemory(path: any, memory: any, key: any): any {
  var encrypted: any = encryptSessionState(memory, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(encrypted, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadApplicationMemory(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "memory": _emptyMemory(), "bounded": true};
  }
  var encrypted: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptSessionState(encrypted, key);
  return {"available": true, "memory": py.get(decrypted, "session", _emptyMemory()), "algorithm": "kaalka", "bounded": true};
}
export function _emptyMemory(): any {
  return {"workflows": {}, "forms": {}, "action_graphs": {}, "navigation_flows": {}, "dashboard_structures": {}, "bounded": true};
}
export { decryptSessionState, encryptSessionState };
