/**
 * Converted from Python: core/crypto/kaalka_wrapper.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function kaalkaEncrypt(data_bytes: any, time_key: any): any {
  var result: any[] = [];
  var length_mod: any = py.mod(py.len(data_bytes), 251);
  var i: any;
  var n: any;
  for ([i, n] of py.enumerate(data_bytes)) {
    var tk: any = py.bitand(((time_key) >> (py.mod(i, 8))), 255);
    var val: any = py.mod(py.add(py.add(py.bitxor(n, tk), py.mul(i, 31)), length_mod), 256);
    val = py.mod(py.add(py.mod(val, 256), 256), 256);
    py.listAppend(result, val);
  }
  return new py.PyBytes(result);
}
export function graphFingerprint(graph: any): any {
  var raw: any = py.encode(py.jsonDumps(graph, {sortKeys: true}));
  return kaalkaEncrypt(raw, 123456);
}
