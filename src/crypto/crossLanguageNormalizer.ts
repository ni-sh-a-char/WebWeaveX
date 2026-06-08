/**
 * Converted from Python: core/crypto/cross_language_normalizer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function normalizeValue(v: any): any {
  if ((typeof v === "number")) {
    return py.toFloat(`${py.format(v, `.12g`)}`);
  }
  if ((Array.isArray(v))) {
    return py.iter(v).map((x: any) => normalizeValue(x));
  }
  if (((v !== null && typeof v === "object" && !Array.isArray(v) && !(v instanceof Set) && !(v instanceof Map)))) {
    return Object.fromEntries(py.iter(py.sorted(py.keys(v))).map((k: any) => ([k, normalizeValue(py.at(v, k))] as [any, any])));
  }
  return v;
}
