/**
 * Converted from Python: core/evidence/corroboration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function corroborateSources(claims: any): any {
  var by_key: Record<string, any> = {};
  var claim: any;
  for (claim of py.iter(py.or2(claims, () => ([])))) {
    if (!((claim !== null && typeof claim === "object" && !Array.isArray(claim) && !(claim instanceof Set) && !(claim instanceof Map)))) {
      continue;
    }
    var key: any = py.toStr(py.get(claim, "key", ""));
    var src: any = py.toStr(py.get(claim, "source", ""));
    if ((py.truthy(key) && py.truthy(src))) {
      py.listAppend(py.setdefault(by_key, key, []), src);
    }
  }
  var corroborated: any[] = [];
  var sources: any;
  for ([key, sources] of py.iter(py.sorted(py.items(by_key)))) {
    var unique: any = py.sorted(py.toSet(sources));
    py.listAppend(corroborated, {"key": key, "sources": unique, "corroboration_count": py.len(unique), "agreement": (py.len(unique) > 1)});
  }
  return {"corroborated": corroborated, "evidence": ["source_corroboration"]};
}
