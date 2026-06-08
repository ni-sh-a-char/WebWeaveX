/**
 * Converted from Python: core/reconstruction/runtime_snapshot_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptValue, encryptValue } from "../crypto/kaalkaRuntimeEngine.js";

export function captureReconstructionSnapshot(state: any): any {
  return {"state": py.pyDict(state), "topology": py.pyDict(py.get(state, "topology", {})), "identities": py.pyDict(py.get(state, "identities", {})), "workflows": [...py.iter(py.get(state, "workflows", []))], "replay_chains": [...py.iter(py.get(state, "replay_chains", []))], "captured": true, "bounded": true};
}
export function restoreReconstructionSnapshot(snapshot: any): any {
  var body: any = py.get(snapshot, "state", snapshot);
  return {"state": py.pyDict(body), "topology": py.pyDict(py.get(snapshot, "topology", py.get(body, "topology", {}))), "identities": py.pyDict(py.get(snapshot, "identities", py.get(body, "identities", {}))), "workflows": [...py.iter(py.get(snapshot, "workflows", py.get(body, "workflows", [])))], "replay_chains": [...py.iter(py.get(snapshot, "replay_chains", py.get(body, "replay_chains", [])))], "restored": true, "bounded": true};
}
export function saveReconstructionSnapshot(path: any, snapshot: any, key: any): any {
  var payload: any = py.jsonDumps(snapshot, {sortKeys: true});
  var encrypted: any = encryptValue(payload, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps({"encrypted": py.at(encrypted, "encrypted"), "algorithm": "kaalka"}, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadReconstructionSnapshot(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "snapshot": _emptySnapshot(), "bounded": true};
  }
  var wrapper: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptValue(py.at(wrapper, "encrypted"), key);
  var snapshot: any = py.jsonLoads(py.at(decrypted, "decrypted"));
  return {"available": true, "snapshot": snapshot, "algorithm": "kaalka", "bounded": true};
}
export function _emptySnapshot(): any {
  return {"state": {}, "topology": {}, "identities": {}, "workflows": [], "replay_chains": [], "bounded": true};
}
export { decryptValue, encryptValue };
