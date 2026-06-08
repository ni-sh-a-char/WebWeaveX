/**
 * Converted from Python: core/causality/causal_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptValue, encryptValue } from "../crypto/kaalkaRuntimeEngine.js";

export function saveCausalMemory(path: any, memory: any, key: any): any {
  var payload: any = py.jsonDumps(memory, {sortKeys: true});
  var encrypted: any = encryptValue(payload, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps({"encrypted": py.at(encrypted, "encrypted"), "algorithm": "kaalka"}, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadCausalMemory(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "memory": _emptyMemory(), "bounded": true};
  }
  var wrapper: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptValue(py.at(wrapper, "encrypted"), key);
  var memory: any = py.jsonLoads(py.at(decrypted, "decrypted"));
  return {"available": true, "memory": memory, "algorithm": "kaalka", "bounded": true};
}
export function rememberCausalRuntime(memory: any, update: any): any {
  var merged: any = py.pyDict(memory);
  var field: any;
  for (field of py.iter(["event_chains", "runtime_propagation", "causal_graphs", "distributed_workflows", "synchronization_state"])) {
    py.setdefault(merged, field, py.get(update, field, py.get(merged, field, {})));
  }
  py.update(merged, update);
  py.setItem(merged, "bounded", true);
  return merged;
}
export function _emptyMemory(): any {
  return {"event_chains": {}, "runtime_propagation": {}, "causal_graphs": {}, "distributed_workflows": {}, "synchronization_state": {}, "bounded": true};
}
export { decryptValue, encryptValue };
