/**
 * Converted from Python: core/memory/runtime_memory_persistence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptValue, encryptValue } from "../crypto/kaalkaRuntimeEngine.js";

export function saveRuntimeMemory(path: any, memory: any, key: any): any {
  var payload: any = py.jsonDumps(memory, {sortKeys: true});
  var encrypted: any = encryptValue(payload, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps({"encrypted": py.at(encrypted, "encrypted"), "algorithm": "kaalka"}, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadRuntimeMemory(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "memory": _emptyStore(), "bounded": true};
  }
  var wrapper: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptValue(py.at(wrapper, "encrypted"), key);
  var memory: any = py.jsonLoads(py.at(decrypted, "decrypted"));
  return {"available": true, "memory": memory, "algorithm": "kaalka", "bounded": true};
}
export function _emptyStore(): any {
  return {"runtime": {}, "knowledge": {}, "semantic": {}, "index": {}, "graph": {}, "lineage": {}, "bounded": true};
}
export { decryptValue, encryptValue };
