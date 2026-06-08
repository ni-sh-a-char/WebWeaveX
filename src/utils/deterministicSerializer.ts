/**
 * Converted from Python: core/utils/deterministic_serializer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _normStr(value: any): any {
  return py.uniNormalize("NFC", value);
}
export function _stable(value: any): any {
  if (((value !== null && typeof value === "object" && !Array.isArray(value) && !(value instanceof Set) && !(value instanceof Map)))) {
    return Object.fromEntries(py.iter(py.sorted(py.keys(value), {key: ((x: any) => _normStr(py.toStr(x))) as (item: any) => any})).map((k: any) => ([k, _stable(py.at(value, k))] as [any, any])));
  }
  if ((Array.isArray(value))) {
    var normalized: any = py.iter(value).map((v: any) => _stable(v));
    return py.sorted(normalized, {key: ((x: any) => py.jsonDumps(x, {sortKeys: true, separators: [",", ":"] as [string, string], ensureAscii: false})) as (item: any) => any});
  }
  if ((typeof value === "string")) {
    return _normStr(value);
  }
  return value;
}
export function dumpsDeterministic(value: any): any {
  return py.jsonDumps(_stable(value), {sortKeys: true, separators: [",", ":"] as [string, string], ensureAscii: false});
}
