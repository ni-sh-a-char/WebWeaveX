/**
 * Converted from Python: core/interaction/interaction_replay_store.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";

export function saveInteractionReplay(path: any, interactions: any, key: any): any {
  var payload: any = {"interactions": [...py.iter(interactions)], "bounded": true};
  var encrypted: any = encryptSessionState(payload, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(encrypted, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadInteractionReplay(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "interactions": [], "bounded": true};
  }
  var encrypted: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptSessionState(encrypted, key);
  var session_payload: any = py.get(decrypted, "session", {});
  return {"available": true, "interactions": [...py.iter(py.get(session_payload, "interactions", []))], "algorithm": "kaalka", "bounded": true};
}
export { decryptSessionState, encryptSessionState };
