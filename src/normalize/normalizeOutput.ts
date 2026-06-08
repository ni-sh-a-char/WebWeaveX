/**
 * Converted from Python: core/normalize/normalize_output.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { emptyNormalized } from "../schemas/normalizedSchema.js";

export function _sortValue(value: any): any {
  if (((value !== null && typeof value === "object" && !Array.isArray(value) && !(value instanceof Set) && !(value instanceof Map)))) {
    return Object.fromEntries(py.iter(py.sorted(py.keys(value))).map((k: any) => ([k, _sortValue(py.at(value, k))] as [any, any])));
  }
  if ((Array.isArray(value))) {
    var normalized: any = py.iter(value).map((v: any) => _sortValue(v));
    return py.sorted(normalized, {key: ((x: any) => py.jsonDumps(x, {sortKeys: true, ensureAscii: true})) as (item: any) => any});
  }
  return value;
}
export function normalizeOutput(parts: any, source_url: any = ""): any {
  var out: any = emptyNormalized(source_url);
  var key: any;
  for (key of py.iter(["content", "code", "dependencies", "metadata", "relationships"])) {
    if ((py.contains(parts, key) && ((py.at(parts, key) !== null && typeof py.at(parts, key) === "object" && !Array.isArray(py.at(parts, key)) && !(py.at(parts, key) instanceof Set) && !(py.at(parts, key) instanceof Map))))) {
      py.setItem(out, key, _sortValue(py.at(parts, key)));
    }
  }
  py.setItem(out, "raw_text", py.toStr(py.or2(py.get(parts, "raw_text", ""), () => (""))));
  py.setItem(out, "source_url", py.or2(source_url, () => (py.toStr(py.or2(py.get(parts, "source_url", ""), () => (""))))));
  py.setItem(out, "fingerprint", py.toStr(py.or2(py.get(parts, "fingerprint", ""), () => (""))));
  return out;
}
export { emptyNormalized };
