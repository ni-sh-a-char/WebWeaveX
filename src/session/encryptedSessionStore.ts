/**
 * Converted from Python: core/session/encrypted_session_store.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";

export function saveEncryptedSession(path: any, session: any, key: any): any {
  var payload: any = encryptSessionState(session, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(payload, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadEncryptedSession(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "session": {"cookies": [], "headers": {}, "auth_tokens": [], "local_storage": {}, "session_storage": {}, "authenticated": false, "bounded": true}, "bounded": true};
  }
  try {
    var payload: any = py.jsonLoads(target.read_text("utf-8"));
  } catch (exc: any) {
    return {"available": false, "reason": py.slice(py.toStr(exc), null, 200), "session": {"cookies": [], "headers": {}, "auth_tokens": [], "bounded": true}, "bounded": true};
  }
  var decrypted: any = decryptSessionState(payload, key);
  return {"available": true, "session": py.get(decrypted, "session", {}), "algorithm": "kaalka", "bounded": true};
}
export { decryptSessionState, encryptSessionState };
