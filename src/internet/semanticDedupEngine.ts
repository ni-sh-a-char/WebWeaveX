/**
 * Converted from Python: core/internet/semantic_dedup_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _fingerprint(text: any): any {
  var normalized: any = py.join(" ", py.split(String(py.or2(text, () => (""))).toLowerCase()));
  return py.hashNew("sha256", py.encode(normalized, "utf-8")).hexdigest();
}
export function semanticDedup(texts: any): any {
  var seen: Record<string, any> = {};
  var t: any;
  for (t of py.iter(py.or2(texts, () => ([])))) {
    var fp: any = _fingerprint(t);
    if (!py.contains(seen, fp)) {
      py.setItem(seen, fp, t);
    }
  }
  return py.iter(py.sorted(seen)).map((k: any) => py.at(seen, k));
}
