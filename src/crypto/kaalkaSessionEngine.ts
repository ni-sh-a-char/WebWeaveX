/**
 * Converted from Python: core/crypto/kaalka_session_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptValue, encryptValue } from "./kaalkaRuntimeEngine.js";

export let MAX_SESSION_BYTES: any = 10000000;
export function encryptSessionState(session: any, key: any): any {
  var serialized: any = py.slice(py.jsonDumps(session, {sortKeys: true, separators: [",", ":"] as [string, string], ensureAscii: false}), null, MAX_SESSION_BYTES);
  var encrypted: any = encryptValue(serialized, key);
  return {...(encrypted), "payload_type": "session", "bounded": true};
}
export function decryptSessionState(payload: any, key: any): any {
  var ciphertext: any = py.toStr(py.get(payload, "encrypted", ""));
  var decrypted: any = decryptValue(ciphertext, key);
  var text: any = py.toStr(py.get(decrypted, "decrypted", ""));
  var session: any = py.jsonLoads(py.slice(text, null, MAX_SESSION_BYTES));
  return {"session": session, "algorithm": "kaalka", "deterministic": true, "bounded": true};
}
export { decryptValue, encryptValue };
