/**
 * Converted from Python: core/crypto/kaalka_archive_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHashPayload } from "./kaalkaHashEngine.js";
import { decryptValue, encryptValue } from "./kaalkaRuntimeEngine.js";

export let MAX_ARCHIVE_BYTES: any = 50000000;
export function encryptExtractionArchive(data: any, key: any): any {
  var serialized: any = py.slice(py.jsonDumps(data, {sortKeys: true, separators: [",", ":"] as [string, string], ensureAscii: false}), null, MAX_ARCHIVE_BYTES);
  var encrypted: any = encryptValue(serialized, key);
  var content_hash: any = computeKaalkaHashPayload(data);
  return {...(encrypted), "payload_type": "extraction_archive", "content_hash": content_hash, "bounded": true};
}
export function decryptExtractionArchive(payload: any, key: any): any {
  var ciphertext: any = py.toStr(py.get(payload, "encrypted", ""));
  var decrypted: any = decryptValue(ciphertext, key);
  var text: any = py.toStr(py.get(decrypted, "decrypted", ""));
  var archive: any = py.jsonLoads(py.slice(text, null, MAX_ARCHIVE_BYTES));
  var content_hash: any = computeKaalkaHashPayload(archive);
  return {"archive": archive, "content_hash": content_hash, "algorithm": "kaalka", "deterministic": true, "bounded": true};
}
export { computeKaalkaHashPayload, decryptValue, encryptValue };
