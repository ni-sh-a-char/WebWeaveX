/**
 * Converted from Python: core/crypto/kaalka_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { dumpsDeterministic } from "../serialize/deterministicSerializer.js";

var kaalka: any = null;
kaalka = null;
export function _safeByte(value: any): any {
  return py.mod(py.add(py.mod(value, 256), 256), 256);
}
export function _deriveTimeKey(token: any, idx: any): any {
  if (!py.truthy(token)) {
    return 0;
  }
  return py.at(token, py.mod(idx, py.len(token)));
}
export function kaalkaEncryptBytes(data: any, token: any): any {
  var encrypted: any[] = [];
  var ln_mod: any = py.mod(py.len(data), 251);
  var i: any;
  var n: any;
  for ([i, n] of py.enumerate(data)) {
    var tk: any = _deriveTimeKey(token, i);
    var value: any = py.mod(py.add(py.add(py.bitxor(n, tk), py.mul(i, 31)), ln_mod), 256);
    py.listAppend(encrypted, _safeByte(value));
  }
  return new py.PyBytes(encrypted);
}
export function hexFingerprint(payload: any, token: any = "webweavex"): any {
  if ((typeof payload === "string" || (payload instanceof py.PyBytes))) {
    var raw_text: any = (((payload instanceof py.PyBytes)) ? py.decode(payload, "utf-8") : payload);
  } else {
    raw_text = dumpsDeterministic(payload);
  }
  var raw: any = py.encode(raw_text, "utf-8");
  return kaalkaEncryptBytes(raw, py.encode(token, "utf-8")).hex();
}
export let fingerprint: any = hexFingerprint;
export let fingerprintV2: any = hexFingerprint;
export let fingerprintV3: any = hexFingerprint;
export { dumpsDeterministic };
